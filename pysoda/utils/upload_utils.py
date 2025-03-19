import requests
import time
import boto3
from configparser import ConfigParser
from os.path import expanduser, join
from .exceptions import ConfigProfileNotSet, FailedToFetchPennsieveDatasets, PennsieveDatasetCannotBeFound


from ..constants import PENNSIEVE_URL

userpath = expanduser("~")
configpath = join(userpath, ".pennsieve", "config.ini")

def generate_options_set(soda_json_structure):
    return "generate-dataset" in soda_json_structure.keys()

def generating_locally(soda_json_structure):
    return soda_json_structure["generate-dataset"]["destination"] == "local"

def generating_on_ps(soda_json_structure):
    return soda_json_structure["generate-dataset"]["destination"] == "bf"

def uploading_with_ps_account(soda_json_structure):
    return "bf-account-selected" in soda_json_structure

def uploading_to_existing_ps_dataset(soda_json_structure):
    return "bf-dataset-selected" in soda_json_structure

def can_resume_prior_upload(resume_status):
    global ums 
    return resume_status and ums.df_mid_has_progress()

def virtual_dataset_empty(soda_json_structure):
    return (
        "dataset-structure" not in soda_json_structure
        and "metadata-files" not in soda_json_structure
        )

def get_dataset_id(dataset_name_or_id):
    """
    Returns the dataset ID for the given dataset name.
    If the dataset ID was provided instead of the name, the ID will be returned. *Common for Guided Mode*
    
    Input:
        dataset_name_or_id: Pennsieve dataset name or ID to get the ID for
    """
    # If the input is already a dataset ID, return it
    if dataset_name_or_id.startswith("N:dataset:"):
        return dataset_name_or_id
    
    # Attempt to retrieve the user's dataset list from Pennsieve
    dataset_list = get_users_dataset_list()    
    
    # Iterate through the user's dataset list to find a matching dataset name
    for dataset in dataset_list:
        if dataset["content"]["name"] == dataset_name_or_id:
            return dataset["content"]["id"]
    
    # If no matching dataset is found, abort with a 404 status and a specific error message
    raise PennsieveDatasetCannotBeFound(dataset_name_or_id)
    # abort(404, "Please select a valid Pennsieve dataset.")


def get_users_dataset_list():
    """
        Returns a list of datasets the user has access to.
        Input:
            token: Pennsieve access token
    """

    # The number of datasets to retrieve per chunk
    NUMBER_OF_DATASETS_PER_CHUNK = 200
    # The total number of datasets the user has access to (set after the first request)
    NUMBER_OF_DATASETS_USER_HAS_ACCESS_TO = None

    # The offset is the number of datasets to skip before retrieving the next chunk of datasets (starts at 0, then increases by the number of datasets per chunk)
    current_offset = 0
    # The list of datasets the user has access to (datasets are added to this list after each request and then returned)
    datasets = []

    try:
        # Get the first chunk of datasets as well as the total number of datasets the user has access to
        r = requests.get(f"{PENNSIEVE_URL}/datasets/paginated", headers=create_request_headers(get_access_token()), params={"offset": current_offset, "limit": NUMBER_OF_DATASETS_PER_CHUNK})
        r.raise_for_status()
        responseJSON = r.json()
        datasets.extend(responseJSON["datasets"])
        NUMBER_OF_DATASETS_USER_HAS_ACCESS_TO = responseJSON["totalCount"]

        # If the number of datasets the user has access to is less than the number of datasets per chunk, we don't need to retrieve any more datasets
        if NUMBER_OF_DATASETS_USER_HAS_ACCESS_TO < NUMBER_OF_DATASETS_PER_CHUNK:
            return datasets
        
        # Otherwise, we need to retrieve the rest of the datasets.
        # We do this by retrieving chunks of datasets until the number of datasets retrieved is equal to the number of datasets the user has access to
        while len(datasets) < NUMBER_OF_DATASETS_USER_HAS_ACCESS_TO:
            # Increase the offset by the number of datasets per chunk (e.g. if 200 datasets per chunk, then increase the offset by 200)
            current_offset += NUMBER_OF_DATASETS_PER_CHUNK
            r = requests.get(f"{PENNSIEVE_URL}/datasets/paginated", headers=create_request_headers(get_access_token()), params={"offset": current_offset, "limit": NUMBER_OF_DATASETS_PER_CHUNK})
            r.raise_for_status()
            responseJSON = r.json()
            datasets.extend(responseJSON["datasets"])

        return datasets
    except Exception as e:
        raise FailedToFetchPennsieveDatasets("Error: Failed to retrieve datasets from Pennsieve. Please try again later.")



def create_request_headers(ps_or_token):
    """
    Creates necessary HTTP headers for making Pennsieve API requests.
    Input: 
        ps: Pennsieve object for a user that has been authenticated
    """
    if type(ps_or_token) == str:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ps_or_token}",
        }
    
    return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ps_or_token.get_user().session_token}",
    }


def get_access_token(api_key=None, api_secret=None):
    """
        Creates a temporary access token for utilizing the Pennsieve API. Reads the api token and secret from the Pennsieve config.ini file.
        get cognito config . If no target profile name is provided the default profile is used. 
    """
    global cached_access_token, last_fetch_time, TOKEN_CACHE_DURATION # Variables used for token caching
    # global namespace_logger
    current_time = time.time()

    # If the cached_access_token is not None and the last fetch time is less than the cache duration, return the cached access token
    if cached_access_token and current_time - last_fetch_time < TOKEN_CACHE_DURATION:
        return cached_access_token
    
    r = requests.get(f"{PENNSIEVE_URL}/authentication/cognito-config")
    r.raise_for_status()

    cognito_app_client_id = r.json()["tokenPool"]["appClientId"]
    cognito_region_name = r.json()["region"]

    cognito_idp_client = boto3.client(
        "cognito-idp",
        region_name=cognito_region_name,
        aws_access_key_id="",
        aws_secret_access_key="",
    )

    # use the default profile values for auth if no api_key or api_secret is provided
    if api_key is None or api_secret is None:
        api_key = get_profile_name_from_api_key("api_token")
        api_secret = get_profile_name_from_api_key("api_secret")


    login_response = cognito_idp_client.initiate_auth(
    AuthFlow="USER_PASSWORD_AUTH",
    AuthParameters={"USERNAME": api_key, "PASSWORD": api_secret},
    ClientId=cognito_app_client_id,
    )

    cached_access_token = login_response["AuthenticationResult"]["AccessToken"]
    last_fetch_time = current_time

    return cached_access_token

def get_profile_name_from_api_key(key):
    config = ConfigParser()
    config.read(configpath)
    if "global" not in config:
        raise ConfigProfileNotSet("global")

    keyname = config["global"]["default_profile"]

    if keyname in config and key in config[keyname]:
        return config[keyname][key]
    return None
