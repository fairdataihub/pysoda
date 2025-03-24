from .constants import METADATA_UPLOAD_PS_PATH
from os.path import join, getsize
from .helpers import upload_metadata_file


# this function saves and uploads the README/CHANGES to Pennsieve, just when users choose to generate onto Pennsieve
## (not used for generating locally)
def create_excel(soda, file_type):
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