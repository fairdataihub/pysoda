from .constants import METADATA_UPLOAD_PS_PATH, TEMPLATE_PATH, SDS_FILE_MANIFEST, SCHEMA_NAME_MANIFEST
from .excel_utils import rename_headers, excel_columns
from openpyxl.styles import PatternFill
from os.path import join, getsize
from openpyxl import load_workbook
import shutil
from ...utils import validate_schema
from .helpers import upload_metadata_file
import os


def create_excel(soda, upload_boolean, local_destination):
    source = join(TEMPLATE_PATH, SDS_FILE_MANIFEST)

    destination = join(METADATA_UPLOAD_PS_PATH, SDS_FILE_MANIFEST) if upload_boolean else local_destination

    shutil.copyfile(source, destination)

    wb = load_workbook(destination)
    ws1 = wb["Sheet1"]

    manifest = soda["dataset_metadata"]["manifest_files"]

    validate_schema(manifest, SCHEMA_NAME_MANIFEST)

    # get the ascii column headers
    row = 2
    ascii_headers = excel_columns(start_index=0)
    manifest_entries = manifest["data"]
    for row in manifest_entries:
      ascii_header_idx = 0 
      for col_data in row:
        if isinstance(col_data, list):
            # space separwte the list into a string
            col_data = " ".join(col_data)
        ws1[ascii_headers[ascii_header_idx] + str(row)] = col_data
        ascii_header_idx += 1
      row += 1

    print(destination)
    wb.save(destination)

    size = getsize(destination)

    ## if generating directly on Pennsieve, call upload function
    if upload_boolean:
        upload_metadata_file(SDS_FILE_MANIFEST, soda,  destination, True)

    return {"size": size}


def load_existing_manifest_file(manifest_file_path):
   # check that a file exists at the path 
    if not os.path.exists(manifest_file_path):
        raise FileNotFoundError(f"Manifest file not found at {manifest_file_path}")
    
   # load the xlsx file and store its first row as a headers array and the rest of the rows in a data key 
    wb = load_workbook(manifest_file_path)
    ws1 = wb["Sheet1"]
    headers = []
    data = []

    for row in ws1.iter_rows(min_row=1, max_row=1, values_only=True):
        headers = list(row)

    for row in ws1.iter_rows(min_row=2, values_only=True):
        data.append(list(row))

    return {"headers": headers, "data": data}

# soda = {
#     "generate-dataset": {
#         "destination": "local",
#         "generate-option": "new",
#         "dataset-name": "test_dataset",
#         "path": "/Users/aaronm",
#         "if-existing": ""
#     },
#     "dataset-structure": {
#         "folders": {
#             "primary": {
#                 "folders": {},
#                 "files": {
#                     "validation_progress.txt": {
#                         "location": "local",
#                         "path": "/Users/aaronm/gmps-11/primary/pool-1/validation_progress.txt",

#                         "action": ["new"],
#                     },
#                     "clean_metadata.py": {
#                         "location": "local",

#                         "path": "/Users/aaronm/gmps-11/primary/pool-1/sub-1/clean_metadata.py",
#                         "action": ["new"]
#                     }
#                 }
#             }
#         }, 
#         "files":  {
#             "metadata.xlsx": {
#                 "location": "local",
#                 "path": "/Users/aaronm/gmps-11/primary/metadata.xlsx",

#                 "action": ["new"]
#             }
#         },
#         "relativePath": "/"
#     },
#     "dataset_metadata": {
#       "manifest_files": {
#           "data": {
#               "headers": [                  
#                     "filename",
#                     "timestamp",
#                     "description",
#                     "file type",
#                     "entity",
#                     "data modality",
#                     "also in dataset",
#                     "also in dataset path",
#                     "data dictionary path",
#                     "entity is transitive",
#                     "Additional Metadata"
#               ],
#               "data": [
#                   [
#                       "metadata.xlsx",
#                       "",
#                       "",
#                       ".xlsx",
#                       "subject-1",
#                       "",
#                       "",
#                       "",
#                       "",
#                       "",
#                       ""
#                   ],
#                   [
#                       "validation_progress.txt",
#                       "",
#                       "",
#                       "",
#                       "",
#                       "",
#                       "",
#                       "",
#                       "",
#                       "",
#                       ""
#                   ],
#                   [
#                       "clean_metadata.py",
#                       "",
#                       "",
#                       "",
#                       "",
#                       "",
#                       "",
#                       "",
#                       "",
#                       "",
#                       ""
#                   ]
#               ]
#           }
#       }
#     }
# }


# try:
#   create_excel(soda, False, "manifest.xlsx")
# except Exception as e:
#   print(e)

