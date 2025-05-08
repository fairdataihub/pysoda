from .constants import METADATA_UPLOAD_PS_PATH, TEMPLATE_PATH, SDS_FILE_MANIFEST, SCHEMA_NAME_MANIFEST
from .excel_utils import rename_headers, excel_columns
from openpyxl.styles import Font, PatternFill
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

    ascii_headers = excel_columns(start_index=0)
    custom_headers_to_column = {}

    orangeFill = PatternFill(
        start_color="FFD965", end_color="FFD965", fill_type="solid"
    )

    # Standard headers from the manifest schema
    standard_headers = [
        "file_name",
        "timestamp",
        "description",
        "file_type",
        "entity",
        "data_modality",
        "also_in_dataset",
        "also_in_dataset_path",
        "data_dictionary_path",
        "entity_is_transitive",
        "additional_metadata",
    ]

    # Populate the Excel file with the data
    for entry in manifest["data"]:
        for idx, header in enumerate(standard_headers):
            value = entry.get(header, "")
            if isinstance(value, list):
                # Convert lists to space-separated strings
                value = " ".join(value)
            ws1[ascii_headers[idx] + str(row)] = value
            ws1[ascii_headers[idx] + str(row)].font = Font(bold=False, size=11, name="Arial")

        # Handle custom fields
        for field_name, field_value in entry.items():
            if field_name in standard_headers:
                continue

            # Check if the field is already in the custom_headers_to_column dictionary
            if field_name not in custom_headers_to_column:
                custom_headers_to_column[field_name] = len(custom_headers_to_column.keys()) + len(standard_headers)

                # Create the column header in the Excel file
                offset_from_final_standard_header = custom_headers_to_column[field_name]
                ws1[ascii_headers[offset_from_final_standard_header] + "1"] = field_name
                ws1[ascii_headers[offset_from_final_standard_header] + "1"].fill = orangeFill
                ws1[ascii_headers[offset_from_final_standard_header] + "1"].font = Font(bold=True, size=12, name="Calibri")

            # Add the field value to the corresponding cell in the Excel file
            offset_from_final_standard_header = custom_headers_to_column[field_name]
            ws1[ascii_headers[offset_from_final_standard_header] + str(row)] = field_value
            ws1[ascii_headers[offset_from_final_standard_header] + str(row)].font = Font(bold=False, size=11, name="Arial")

        row += 1


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
        # grab the item in row 5
        new_row = []
        for col_data in row:
            if isinstance(col_data, list):
                # space separate the list into a string
                col_data = " ".join(col_data)
            new_row.append(col_data)
        data.append(new_row)

    return {"headers": headers, "data": data}


