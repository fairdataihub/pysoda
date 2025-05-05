import pkg_resources
import json
from jsonschema import validate
import os.path



def load_schema(schema_name):
    # Get the current directory of this file
    current_dir = os.path.dirname(__file__)
    
    # Construct the path to the schema directory one level up
    schema_path = os.path.join(current_dir, "..", 'schema', schema_name)
    
    # Normalize the path
    schema_path = os.path.abspath(schema_path)
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)
    return schema

# TODO: Make an enum of the schema names and add extensions to the schema names in the function.....or to the enum.
def validate_schema(schema, schema_name):
    """
    Validate submission metadata against the submission schema.

    Args:
        schema (dict): The python dictionary version of the schema or subschema to validate against the json schema.
        schema_name (str): The file name of the schema to validate against.

    Raises:
        ValidationError: If the metadata is invalid.
    """
    print(schema_name)
    true_schema = load_schema(schema_name)
    validate(instance=schema, schema=true_schema)


def get_sds_headers(schema_name):
    """
    Get the headers for the SDS file.

    Args:
        soda (dict): The soda object containing the metadata.
        schema_name (str): The name of the schema to validate against.

    Returns:
        list: The headers for the SDS file.
    """

    true_schema = load_schema(schema_name)
    sds_headers = true_schema["items"][0]["properties"].keys()
    return sds_headers