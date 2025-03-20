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
