from .constants import METADATA_UPLOAD_PS_PATH, TEMPLATE_PATH, SDS_FILE_DATASET_DESCRIPTION, SCHEMA_NAME_DATASET_DESCRIPTION
from os.path import join, getsize
from openpyxl import load_workbook
import shutil
from .excel_utils import rename_headers, excel_columns
import itertools
from openpyxl.styles import PatternFill
from ...utils import validate_schema
from .helpers import upload_metadata_file



def create_excel(
    soda,
    upload_boolean,
    local_destination,
):
    source = join(TEMPLATE_PATH, SDS_FILE_DATASET_DESCRIPTION)
    destination = join(METADATA_UPLOAD_PS_PATH, SDS_FILE_DATASET_DESCRIPTION) if upload_boolean else local_destination
    shutil.copyfile(source, destination)

    validate_schema(soda["dataset_metadata"]["dataset_description"], SCHEMA_NAME_DATASET_DESCRIPTION)

    # write to excel file
    wb = load_workbook(destination)
    ws1 = wb["Sheet1"]

    ws1["D22"] = ""
    ws1["E22"] = ""
    ws1["D24"] = ""
    ws1["E24"] = ""
    ws1["D25"] = ""
    ws1["E25"] = ""

    # Populate the Metadata version (Required)
    ws1["D2"] = soda["dataset_metadata"]["dataset_description"]["metadata_version"]

    # Populate the Dataset Type (default to empty string if not present)
    ws1["D3"] = (
    soda.get("dataset_metadata", {})
        .get("dataset_description", {})
        .get("dataset_type", "")
    )

    populate_standards_info(ws1, soda)



    keyword_array = populate_basic_info(ws1, soda)

    study_array_len = populate_study_info(ws1, soda)

    (funding_array, contributor_role_array) = populate_contributor_info(
        ws1, soda
    )

    related_info_len = populate_related_info(ws1, soda)

    # keywords length
    keyword_len = len(keyword_array)

    # contributors length
    no_contributors = len(contributor_role_array)

    # funding = SPARC award + other funding sources
    funding_len = len(funding_array)

    # obtain length for formatting compliance purpose
    max_len = max(
        keyword_len, funding_len, no_contributors, related_info_len, study_array_len
    )

    rename_headers(ws1, max_len, 3)
    grayout_subheaders(ws1, max_len, 3)
    grayout_single_value_rows(ws1, max_len, 3)

    if ws1["G1"].value == "Value n":
        ws1.delete_cols(7)

    wb.save(destination)

    size = getsize(destination)

    ## if generating directly on Pennsieve, then call upload function and then delete the destination path
    if upload_boolean:
        upload_metadata_file(
            "dataset_description.xlsx", soda, destination, True
        )

    return {"size": size}




def populate_study_info(workbook, soda):
    study_info = soda["dataset_metadata"]["dataset_description"]["study_information"]
    workbook["D11"] = study_info["study_purpose"]
    workbook["D12"] = study_info["study_data_collection"]
    workbook["D13"] = study_info["study_primary_conclusion"]
    workbook["D17"] = study_info["study collection title"]

    ## get study organ system
    for i, column in zip(
        range(len(study_info["study organ system"])), excel_columns(start_index=3)
    ):
        workbook[column + "14"] = study_info["study organ system"][i]
    ## get study approach
    for i, column in zip(
        range(len(study_info["study approach"])), excel_columns(start_index=3)
    ):
        workbook[column + "15"] = study_info["study approach"][i]
    ## get study technique
    for i, column in zip(
        range(len(study_info["study technique"])), excel_columns(start_index=3)
    ):
        workbook[column + "16"] = study_info["study technique"][i]

    return max(
        len(study_info["study organ system"]),
        len(study_info["study approach"]),
        len(study_info["study technique"]),
    )

def populate_standards_info(workbook, soda):
    standards_info = soda["dataset_metadata"]["dataset_description"]["standards_information"]
    workbook["D5"] = standards_info["data_standard"]
    workbook["D6"] = standards_info["data_standard_version"]

    # Write standards array across columns in row 8 (D8, E8, F8, ...)
    standards_array = standards_info["standards"]
    for col, standard in zip(excel_columns(start_index=3), standards_array):
        workbook[f"{col}8"] = standard

    return len(standards_array)


def populate_basic_info(workbook, soda):
    basic_info = soda["dataset_metadata"]["dataset_description"]["basic_information"]
    workbook["D8"] = basic_info["title"]
    workbook["D9"] = basic_info["subtitle"]
    workbook["D10"] = basic_info["description"]
    
    # Write keywords array across columns in row 11 (D11, E11, F11, ...)
    keywords = basic_info["keywords"]
    for col, keyword in zip(excel_columns(start_index=3), keywords):
        workbook[f"{col}11"] = keyword
    
    workbook["D12"] = basic_info["funding"]
    workbook["D13"] = basic_info["acknowledgments"]
    workbook["D14"] = basic_info["license"]

    return keywords




def populate_contributor_info(workbook, soda):
    contributor_info = soda["dataset_metadata"]["dataset_description"]["contributor_information"]
    basic_info = soda["dataset_metadata"]["dataset_description"]["basic_information"]
    ## get award info
    for i, column in zip(
        range(len(basic_info["funding"])), excel_columns(start_index=3)
    ):
        workbook[column + "8"] = basic_info["funding"][i]

    ### get Acknowledgments
    workbook["D9"] = basic_info["acknowledgment"]

    ### get Contributors
    for contributor, column in zip(
        contributor_info, excel_columns(start_index=3)
    ):
        workbook[column + "19"] = contributor["contributor_name"]
        workbook[column + "20"] = contributor["contributor_orcid_id"]
        workbook[column + "21"] = contributor["contributor_affiliation"]
        workbook[column + "22"] = contributor["contributor_role"]

    return [basic_info["funding"], contributor_info]


def populate_related_info(workbook, soda):
    ## get related links including protocols
    related_information = soda["dataset_metadata"]["dataset_description"]["related_information"]
    for info, column in zip(related_information, excel_columns(start_index=3)):
        workbook[column + "24"] = info["identifier_description"]
        workbook[column + "25"] = info["relation_type"]
        workbook[column + "26"] = info["identifier"]
        workbook[column + "27"] = info["identifier_type"]

    return len(related_information)




def grayout_subheaders(workbook, max_len, start_index):
    """
    Gray out sub-header rows for values exceeding 3 (SDS2.0).
    """
    headers_list = ["4", "10", "18", "23", "28"]
    columns_list = excel_columns(start_index=start_index)

    for (i, column), no in itertools.product(zip(range(2, max_len + 1), columns_list[1:]), headers_list):
        cell = workbook[column + no]
        fillColor("B2B2B2", cell)


def grayout_single_value_rows(workbook, max_len, start_index):
    """
    Gray out rows where only single values are allowed. Row number: 2, 3, 5, 6, 9, 11, 12, 13, 17, 29, 30
    """

    columns_list = excel_columns(start_index=start_index)
    row_list = ["2", "3", "5", "6", "9", "11", "12", "13", "17", "29", "30"]
    for (i, column), no in itertools.product(zip(range(2, max_len + 1), columns_list[1:]), row_list):
        cell = workbook[column + no]
        fillColor("CCCCCC", cell)


def fillColor(color, cell):
    colorFill = PatternFill(start_color=color, end_color=color, fill_type="solid")

    cell.fill = colorFill