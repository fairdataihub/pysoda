from constants import METADATA_UPLOAD_BF_PATH, TEMPLATE_PATH
from excel_utils import rename_headers, excel_columns
from openpyxl.styles import PatternFill
from os.path import join, getsize
from openpyxl import load_workbook
import shutil



# TODO: Handle optional entries when coupled with provided entries
# TODO: Handle extending columns and filling with color when more entries are provided than the template default handles
def create_excel(soda, upload, generateDestination):
    source = join(TEMPLATE_PATH, "code_description.xlsx")
    destination = join(METADATA_UPLOAD_BF_PATH, "code_description.xlsx") if upload else generateDestination
    shutil.copyfile(source, destination)


    print(destination)
    wb = load_workbook("./" +destination)
    print(wb.sheetnames)
    ws1 = wb[wb.sheetnames[0]]

    print(ws1)

    populate_input_output_information(ws1, soda)

    populate_basic_information(ws1, soda)


    populate_ten_simple_rules(ws1, soda)


    wb.save(destination)





# TODO: Handle optional entries
def populate_input_output_information(ws1, soda):
    # populate from row 27 and column 4 up to column n, depending upon the amount of items in the array for each input output information entry
    input_output_information = soda["dataset_metadata"]["input_output_information"]

    row = 27

    excel_ascii = excel_columns(start_index=3)[0]
    ws1[excel_ascii + str(row)] = input_output_information["number_of_inputs"]

    for input, column in zip(input_output_information["inputs"], excel_columns(start_index=3)):
        row = 28
        ws1[column + str(row)] = input["input_parameter_name"]
        ws1[column + str(row + 1)] = input["input parameter type"]
        ws1[column + str(row + 2)] = input["input_parameter_description"]
        ws1[column + str(row + 3)] = input["input_units"]
        ws1[column + str(row + 4)] = input["input_default_value"]

    # populate number of outputs into row 34
    row = 34
    ws1[excel_ascii + str(row)] = input_output_information["number_of_outputs"]

    # populate the outputs from row 35 - 39
    for output, column in zip(input_output_information["outputs"], excel_columns(start_index=3)):
        row = 35
        ws1[column + str(row)] = output["output_parameter_name"]
        ws1[column + str(row + 1)] = output["output_parameter_type"]
        ws1[column + str(row + 2)] = output["output_parameter_description"]
        ws1[column + str(row + 3)] = output["output_units"]
        ws1[column + str(row + 4)] = output["output_default_value"]


def populate_basic_information(ws1, soda):
    basic_information = soda["dataset_metadata"]["basic_information"]

    # fill out basic information from row 2 - 5 starting from col 3
    row = 2
    for info, column in zip(basic_information, excel_columns(start_index=3)):
        ws1[column + str(row)] = info["RRID_term"]
        ws1[column + str(row + 1)] = info["RRID_identifier"]
        ws1[column + str(row + 2)] = info["ontology_term"]
        ws1[column + str(row + 3)] = info["ontology_identifier"]


def populate_ten_simple_rules(ws1, soda):
    
    # populate rows 8 - 25 starting from col 3 with the ten simple rules data
    ten_simple_rules = soda["dataset_metadata"]["ten_simple_rules"]

    row = 8

    TSR1 = ten_simple_rules["TSR1"]
    TSR2 = ten_simple_rules["TSR2"]
    TSR3a = ten_simple_rules["TSR3a"]
    TSR3b = ten_simple_rules["TSR3b"]
    TSR3c = ten_simple_rules["TSR3c"]
    TSR4 = ten_simple_rules["TSR4"]
    TSR5 = ten_simple_rules["TSR5"]
    TSR6 = ten_simple_rules["TSR6"]
    TSR7a = ten_simple_rules["TSR7a"]
    TSR7b = ten_simple_rules["TSR7b"]
    TSR7c = ten_simple_rules["TSR7c"]
    TSR7d = ten_simple_rules["TSR7d"]
    TSR7e = ten_simple_rules["TSR7e"]
    TSR8a = ten_simple_rules["TSR8a"]
    TSR8b = ten_simple_rules["TSR8b"]
    TSR9 = ten_simple_rules["TSR9"]
    TSR10a = ten_simple_rules["TSR10a"]
    TSR10b = ten_simple_rules["TSR10b"]

    for rule in [TSR1, TSR2, TSR3a, TSR3b, TSR3c, TSR4, TSR5, TSR6, TSR7a, TSR7b, TSR7c, TSR7d, TSR7e, TSR8a, TSR8b, TSR9, TSR10a, TSR10b]:
        write_tsr_row(rule, row, ws1)
        row += 1

def write_tsr_row(TSR, row, ws1):
    for rule_item, col in zip(TSR, excel_columns(start_index=3)):
        ws1[col + str(row)] = rule_item

soda = {
    "dataset_metadata": {
        "input_output_information": {
            "number_of_inputs": 1,
            "inputs": [
                {
                    "input_parameter_name": "ws1", 
                    "input parameter type": "worksheet",
                    "input_parameter_description": "The worksheet to write to",
                    "input_units": "N/A",
                    "input_default_value": "worksheet",
                },
                {
                    "input_parameter_name": "soda", 
                    "input parameter type": "dictionary",
                    "input_parameter_description": "The soda dictionary",
                    "input_units": "N/A",
                    "input_default_value": "soda",
                },
            ],
            "number_of_outputs": 1,
            "outputs": [
                {
                    "output_parameter_name": "None",
                    "output_parameter_type": "None",
                    "output_parameter_description": "None",
                    "output_units": "N/A",
                    "output_default_value": "N/A",
                }
            ]
        },
        "basic_information": [
            {
                "RRID_term": "RRID:SCR_016755",
                "RRID_identifier": "https://scicrunch.org/resolver/RRID:SCR_016755",
                "ontology_term": "N/A",
                "ontology_identifier": "N/A",
            },
            {
                "RRID_term": "RRID:SCR_016755",
                "RRID_identifier": "https://scicrunch.org/resolver/RRID:SCR_016755",
                "ontology_term": "N/A",
                "ontology_identifier": "N/A",
            }
        ],
        "ten_simple_rules": {
            "TSR1": [
                "https://google.com",
                "3",
                "4",
                "Silly string",
                "All the silly things with silly string"
            ],
            "TSR2": [
                "https://google.com",
                "3",
                "4",
                "Silly string",
                "All the silly things with silly string"
            ],
            "TSR3a": [
                "https://google.com",
                "3",
                "4",
                "Silly string",
                "All the silly things with silly string"
            ],
            "TSR3b": [
                "https://google.com",
            ],
            "TSR3c": [
                "https://google.com",
            ],
            "TSR4": [
                "https://google.com",
                "3",
                "4",
                "Silly string",
                "All the silly things with silly string"
            ],
            "TSR5": [
                "https://google.com",
                "3",
                "4",
                "Silly string",
                "All the silly things with silly string"
            ],
            "TSR6": [
                "https://google.com",
                "3",
                "4",
                "Silly string",
                "All the silly things with silly string"
            ],
            "TSR7a": [
                "https://google.com",
                "3",
                "4",
                "Silly string",
                "All the silly things with silly string"
            ],
            "TSR7b": [
                "https://google.com",
            ],
            "TSR7c": [
                "https://google.com",
            ],
            "TSR7d": [
                "https://google.com",
            ],
            "TSR7e": [
                "https://google.com",
            ],
            "TSR8a": [
                "https://google.com",
                "3",
                "4",
                "Silly string",
                "All the silly things with silly string"
            ],
            "TSR8b": [
                "https://google.com"
            ],
            "TSR9": [
                "https://google.com",
                "3",
                "4",
                "Silly string",
                "All the silly things with silly string"
            ],
            "TSR10a": [
                "https://google.com",
                "3",
                "4",
                "Silly string",
                "All the silly things with silly string"
            ],
            "TSR10b": [
                "https://google.com",
            ]
        }
    }
}

create_excel(soda, False, "code_description.xlsx")


    

