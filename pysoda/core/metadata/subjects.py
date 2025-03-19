from constants import METADATA_UPLOAD_BF_PATH, TEMPLATE_PATH
from excel_utils import rename_headers, excel_columns
from openpyxl.styles import PatternFill
from os.path import join, getsize
from openpyxl import load_workbook
import shutil
from utils import validate_schema

def save_subjects_file(upload_boolean, bfaccount, bfdataset, filepath, datastructure):
    source = join(TEMPLATE_PATH, "subjects.xlsx")

    if upload_boolean:
        destination = join(METADATA_UPLOAD_BF_PATH, "subjects.xlsx")

    else:
        destination = filepath

    shutil.copyfile(source, destination)
    wb = load_workbook(destination)
    ws1 = wb["Sheet1"]

    transposeDatastructure = transposeMatrix(datastructure)

    mandatoryFields = transposeDatastructure[:11]
    optionalFields = transposeDatastructure[11:]
    refinedOptionalFields = getMetadataCustomFields(optionalFields)

    templateHeaderList = subjectsTemplateHeaderList
    sortMatrix = sortedSubjectsTableData(mandatoryFields, templateHeaderList)

    if refinedOptionalFields:
        refinedDatastructure = transposeMatrix(
            np.concatenate((sortMatrix, refinedOptionalFields))
        )
    else:
        refinedDatastructure = transposeMatrix(sortMatrix)
    
    # delete all optional columns first (from the template)
    ws1.delete_cols(12, 18)

    # 1. see if the length of datastructure[0] == length of datastructure. If yes, go ahead. If no, add new columns from headers[n-1] onward.
    headers_no = len(refinedDatastructure[0])
    orangeFill = PatternFill(
        start_color="FFD965", end_color="FFD965", fill_type="solid"
    )

    for column, header in zip(
        excel_columns(start_index=11), refinedDatastructure[0][11:headers_no]
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
            # import pdb; pdb.set_trace()
            cell = column + str(i + 1)
            ws1[cell] = refinedDatastructure[i][j] or ""
            ws1[cell].font = Font(bold=False, size=11, name="Arial")

    wb.save(destination)

    size = getsize(destination)

    ## if generating directly on Pennsieve, then call upload function and then delete the destination path
    if upload_boolean:
        upload_metadata_file("subjects.xlsx", bfaccount, bfdataset, destination, True)

    return size


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

