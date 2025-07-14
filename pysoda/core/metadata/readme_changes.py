from .constants import METADATA_UPLOAD_PS_PATH, TEMPLATE_PATH
from os.path import join, getsize
from .helpers import upload_metadata_file
import shutil


# this function saves and uploads the README/CHANGES to Pennsieve, just when users choose to generate onto Pennsieve
## (not used for generating locally)
def create_text_file(soda, upload_boolean, local_destination, file_type):
    """
    Create a text file for README or CHANGES metadata using a template.

    Args:
        soda (dict): The soda object containing dataset metadata.
        upload_boolean (bool): Whether to upload the file to Pennsieve.
        local_destination (str): The path to save the text file.
        file_type (str): The type of the file to be created, either "README" or "CHANGES".

    Returns:
        dict: A dictionary containing the size of the metadata file.
    """

    template_filename = f"{file_type}.txt"
    source = join(TEMPLATE_PATH, template_filename)
    destination = join(METADATA_UPLOAD_PS_PATH, template_filename) if upload_boolean else local_destination

    # Copy the template to the destination (if it exists)
    try:
        shutil.copyfile(source, destination)
    except FileNotFoundError:
        # If template not found, just create a new file
        with open(destination, "w", encoding="utf-8") as f:
            pass

    # Write the actual content from soda into the file (overwriting template content)
    text = soda["dataset_metadata"].get(file_type, "")
    with open(destination, "w", encoding="utf-8") as file:
        file.write(text)

    size = getsize(destination)
    if upload_boolean:
        upload_metadata_file(template_filename, soda, destination, True)

    return size


