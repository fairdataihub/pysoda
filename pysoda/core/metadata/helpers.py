import requests
from ...constants import PENNSIEVE_URL
from ...utils import get_dataset_id, get_access_token, create_request_headers, connect_pennsieve_client, PennsieveActionNoPermission, GenericUploadError
from ...core import has_edit_permissions
from functools import partial
import time 
import os
from .. import logger
# helper function to process custom fields (users add and name them) for subjects and samples files
def getMetadataCustomFields(matrix):
    return [column for column in matrix if any(column[1:])]


# transpose a matrix (array of arrays)
# The transpose of a matrix is found by interchanging its rows into columns or columns into rows.
# REFERENCE: https://byjus.com/maths/transpose-of-a-matrix/
def transposeMatrix(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

# needed to sort subjects and samples table data to match the UI fields
def sortedSubjectsTableData(matrix, fields):
    sortedMatrix = []
    for field in fields:
        for column in matrix:
            if column[0].lower() == field:
                sortedMatrix.append(column)
                break

    customHeaderMatrix = [
        column for column in matrix if column[0].lower() not in fields
    ]

    return (
        np.concatenate((sortedMatrix, customHeaderMatrix)).tolist()
        if customHeaderMatrix
        else sortedMatrix
    )



def upload_metadata_file(file_name, soda, path_to_file, delete_after_upload=True):
    global logger

    if "ps-account-selected" in soda:
        ps_account = soda["ps-account-selected"]["account-name"]
    
    if "ps-dataset-selected" in soda:
        ps_dataset = soda["ps-dataset-selected"]["dataset-name"]
    
    # check that the Pennsieve dataset is valid
    selected_dataset_id = get_dataset_id(ps_dataset)

    # check that the user has permissions for uploading and modifying the dataset
    if not has_edit_permissions(get_access_token(), selected_dataset_id):
        raise PennsieveActionNoPermission("edit" + selected_dataset_id)
    headers = create_request_headers(get_access_token())
    # handle duplicates on Pennsieve: first, obtain the existing file ID
    r = requests.get(f"{PENNSIEVE_URL}/datasets/{selected_dataset_id}", headers=headers)
    r.raise_for_status()
    ds_items = r.json()
    # go through the content in the dataset and find the file ID of the file to be uploaded
    for item in ds_items["children"]:
        if item["content"]["name"] == file_name:
            item_id = item["content"]["id"]
            jsonfile = {
                "things": [item_id]
            }
            # then, delete it using Pennsieve method delete(id)\vf = Pennsieve()
            r = requests.post(f"{PENNSIEVE_URL}/data/delete",json=jsonfile, headers=headers)
            r.raise_for_status()
    try:
        ps = connect_pennsieve_client(ps_account)
        # create a new manifest for the metadata file
        ps.use_dataset(selected_dataset_id)
        manifest = ps.manifest.create(path_to_file)
        m_id = manifest.manifest_id
    except Exception as e:
        logger.error(e)
        error_message = "Could not create manifest file for this dataset"
        raise GenericUploadError(error_message)
    
    # upload the manifest file
    try: 
        ps.manifest.upload(m_id)
        # create a subscriber function with ps attached so it can be used to unusbscribe
        subscriber_metadata_ps_client = partial(subscriber_metadata, ps)
        # subscribe for the upload to finish
        ps.subscribe(10, False, subscriber_metadata_ps_client)
    except Exception as e:
        logger.error("Error uploading dataset files")
        logger.error(e)
        raise Exception("The Pennsieve Agent has encountered an issue while uploading. Please retry the upload. If this issue persists please follow this <a target='_blank' rel='noopener noreferrer' href='https://docs.sodaforsparc.io/docs/how-to/how-to-reinstall-the-pennsieve-agent'> guide</a> on performing a full reinstallation of the Pennsieve Agent to fix the problem.")


    # before we can remove files we need to wait for all of the Agent's threads/subprocesses to finish
    # elsewise we get an error that the file is in use and therefore cannot be deleted
    time.sleep(5)

    # delete the local file that was created for the purpose of uploading to Pennsieve
    if delete_after_upload:
        os.remove(path_to_file)



def subscriber_metadata(ps, events_dict):
    global logger
    if events_dict["type"] == 1:
        fileid = events_dict["upload_status"].file_id
        total_bytes_to_upload = events_dict["upload_status"].total
        current_bytes_uploaded = events_dict["upload_status"].current
        if current_bytes_uploaded == total_bytes_to_upload and fileid != "":
            logger.info("File upload complete")
            ps.unsubscribe(10)