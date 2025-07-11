from .constants import METADATA_UPLOAD_PS_PATH
from os.path import join, getsize
from .helpers import upload_metadata_file


# this function saves and uploads the README/CHANGES to Pennsieve, just when users choose to generate onto Pennsieve
## (not used for generating locally)
def create_text_file(soda, upload_boolean, local_destination, file_type):
    """
    Create an Excel file for submission metadata.

    Args:
        soda (dict): The soda object containing dataset metadata.
        upload_boolean (bool): Whether to upload the file to Pennsieve.
        destination_path (str): The path to save the Excel file.
        file_type (str): The type of the file to be created, either "README" or "CHANGES".

    Returns:
        dict: A dictionary containing the size of the metadata file.
    """

    text = soda["dataset_metadata"][file_type]

    """ Create the text file and get the size of the file. """
    destination = join(METADATA_UPLOAD_PS_PATH, file_type + ".txt") if upload_boolean else local_destination
    with open(destination, "w") as file:
        file.write(text)
    
    metadata_file_size = getsize(destination)
    if upload_boolean:
        upload_metadata_file(soda, destination, file_type.lower() + ".txt")
        
    return {"metadata_file_size": metadata_file_size}


