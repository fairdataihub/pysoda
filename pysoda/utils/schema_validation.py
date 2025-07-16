import json
from jsonschema import validate
import sys 
import os



def load_schema(schema_name):
    schema_path = get_schema_path(schema_name)
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)
    return schema


def get_schema_path(filename):
    """Get the path to a schema file within the metadata_templates package."""
    
    # Method 1: Try PyInstaller bundle first (onefolder creates _MEIPASS)
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller onefolder extracts to _MEIPASS/
        possible_paths = [
            os.path.join(sys._MEIPASS, "pysoda", "schema", filename),
            os.path.join(sys._MEIPASS, filename)
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
    
    # Method 2: Try to import the metadata_templates module (works if PyPI package is properly installed)
    try:
        from .. import schema
        schema_dir = os.path.dirname(schema.__file__)
        schema_path = os.path.join(schema_dir, filename)
        if os.path.exists(schema_path):
            return schema_path
    except (ImportError, ModuleNotFoundError, AttributeError):
        pass
    
    # Method 3: Search in the Flask app's directory structure
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    
    search_paths = [
        os.path.join(current_dir, '..', '..', 'schema', filename),
        os.path.join(current_dir, 'schema', filename),
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            return path
        
    
    # Method 4: Use importlib_resources (Python 3.7+)
    try:
        from importlib import resources
        with resources.path('schema', filename) as schema_path:
            if schema_path.exists():
                return str(schema_path)
    except (ImportError, ModuleNotFoundError):
        # Fallback to other methods if importlib_resources is not available
        pass
    
    raise ImportError(f"Could not locate or create schema file {filename}.")


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