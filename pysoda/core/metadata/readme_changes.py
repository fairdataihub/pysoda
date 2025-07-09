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

    return True # TEMP
    file_path = join(METADATA_UPLOAD_PS_PATH, file_type)
    text_string = ''

    if file_type == "README.txt":
        text_string = soda["dataset_metadata"]["README"]
    else:
        text_string = soda["dataset_metadata"]["CHANGES"]

    with open(file_path, "w") as f:
        f.write(text_string)

    size = getsize(file_path)

    upload_metadata_file(file_type, soda, file_path, True)

    return { "size": size, "filepath": file_path }