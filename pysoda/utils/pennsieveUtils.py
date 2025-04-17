import requests
from ..constants import PENNSIEVE_URL
from .authentication import get_access_token
import re 
from .exceptions import PennsieveDatasetCannotBeFound, FailedToFetchPennsieveDatasets

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
    

    try:
        # Attempt to retrieve the user's dataset list from Pennsieve
        dataset_list = get_users_dataset_list()
    except Exception as e:
        raise FailedToFetchPennsieveDatasets(str(e))
    
    # Iterate through the user's dataset list to find a matching dataset name
    for dataset in dataset_list:
        if dataset["content"]["name"] == dataset_name_or_id:
            return dataset["content"]["id"]
    
    # If no matching dataset is found, abort with a 404 status and a specific error message
    raise PennsieveDatasetCannotBeFound(dataset_name_or_id)
  

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
        raise e
    





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


forbidden_characters_bf = '\/:*?"<>.,'


def check_forbidden_characters_ps(my_string):
    """
    Check for forbidden characters in Pennsieve file/folder name

    Args:
        my_string: string with characters (string)
    Returns:
        False: no forbidden character
        True: presence of forbidden character(s)
    """
    regex = re.compile(f"[{forbidden_characters_bf}]")
    if regex.search(my_string) == None and "\\" not in r"%r" % my_string:
        return False
    else:
        return True