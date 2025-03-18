import pkg_resources
import json
from jsonschema import validate

def load_schema(schema_name):
    schema_path  = pkg_resources.resource_filename(__name__, f'../../../schema/{schema_name}')
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
    true_schema = load_schema(schema_name)
    validate(instance=schema, schema=true_schema)