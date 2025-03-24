from .constants import METADATA_UPLOAD_PS_PATH, TEMPLATE_PATH, SDS_FILE_SAMPLES, SCHEMA_NAME_SAMPLES
from .excel_utils import rename_headers, excel_columns
from openpyxl.styles import PatternFill
from os.path import join, getsize
from openpyxl import load_workbook
import shutil
from ...utils import validate_schema
from .helpers import transposeMatrix, getMetadataCustomFields, sortedSubjectsTableData
from openpyxl.styles import Font
import numpy as np

def create_excel(soda, upload_boolean, filepath):
    source = join(TEMPLATE_PATH, SDS_FILE_SAMPLES)

    if upload_boolean:
        destination = join(METADATA_UPLOAD_PS_PATH, SDS_FILE_SAMPLES)

    else:
        destination = filepath

    shutil.copyfile(source, destination)

    wb = load_workbook(destination)
    ws1 = wb["Sheet1"]

    datastructure = soda["dataset_metadata"]["samples"]

    validate_schema(datastructure, SCHEMA_NAME_SAMPLES)

    transposeDatastructure = transposeMatrix(datastructure)

    mandatoryFields = transposeDatastructure[:9]
    optionalFields = transposeDatastructure[9:]
    refinedOptionalFields = getMetadataCustomFields(optionalFields)

    templateHeaderList = samplesTemplateHeaderList
    sortMatrix = sortedSubjectsTableData(mandatoryFields, templateHeaderList)

    if refinedOptionalFields:
        refinedDatastructure = transposeMatrix(
            np.concatenate((sortMatrix, refinedOptionalFields))
        )
    else:
        refinedDatastructure = transposeMatrix(sortMatrix)

    ws1.delete_cols(10, 15)

    # 1. see if the length of datastructure[0] == length of datastructure. If yes, go ahead. If no, add new columns from headers[n-1] onward.
    headers_no = len(refinedDatastructure[0])
    orangeFill = PatternFill(
        start_color="FFD965", end_color="FFD965", fill_type="solid"
    )

    for column, header in zip(
        excel_columns(start_index=9), refinedDatastructure[0][9:headers_no]
    ):
        cell = column + str(1)
        ws1[cell] = header
        ws1[cell].fill = orangeFill
        ws1[cell].font = Font(bold=True, size=12, name="Calibri")

    # 2. populate matrices
    for i, item in enumerate(refinedDatastructure):
        if i == 0:
            continue
        for column, j in zip(excel_columns(start_index=0), range(len(item))):
            cell = column + str(i + 1)
            ws1[cell] = refinedDatastructure[i][j] or ""
            ws1[cell].font = Font(bold=False, size=11, name="Arial")

    wb.save(destination)

    size = getsize(destination)

    ## if generating directly on Pennsieve, call upload function
    # if upload_boolean:
    #     upload_metadata_file("samples.xlsx", bfaccount, bfdataset, destination, True)

    return {"size": size}


samplesTemplateHeaderList = [
            "sample id",
            "subject id",
            "was derived from",
            "pool id",
            "sample experimental group",
            "sample type",
            "sample anatomical location",
            "also in dataset",
            "member of",
            "metadata only",
            "laboratory internal id",
            "date of derivation",
            "experimental log file path",
            "reference atlas",
            "pathology",
            "laterality",
            "cell type",
            "plane of section",
            "protocol title",
            "protocol url or doi"
        ]





