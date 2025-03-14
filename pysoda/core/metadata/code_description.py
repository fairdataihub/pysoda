from .constants import METADATA_UPLOAD_BF_PATH, TEMPLATE_PATH
from .excel_utils import rename_headers, excel_columns
from openpyxl.styles import PatternFill
from os.path import join, getsize
from openpyxl import load_workbook
import shutil




def create_excel(soda, upload, generateDestination):
    source = join(TEMPLATE_PATH, "code_description.xlsx")
    destination = join(METADATA_UPLOAD_BF_PATH, "code_description.xlsx") if upload else generateDestination
    shutil.copyfile(source, destination)


    wb = load_workbook(destination)
    ws1 = wb["Sheet1"]

    populate_input_output_information(ws1, soda)





def populate_input_output_information(ws1, soda):
    # populate from row 27 and column 4 up to column n, depending upon the amount of items in the array for each input output information entry
    input_output_information = soda["dataset_metadata"]["input_output_information"]

    row = 27
    column = 4

    

