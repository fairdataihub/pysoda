from os.path import join, getsize, abspath, dirname



TEMPLATE_PATH = join(dirname(abspath(__file__)), '..', 'metadata_templates')
METADATA_UPLOAD_BF_PATH = join(dirname(abspath(__file__)), 'metadata_upload_bf')


SCHEMA_NAMES = {
    "submission": "submission_schema.json",
    "subjects": "subjects_schema.json"
}


SDS_FILE_SUBJECTS = "subjects.xlsx"
SCHEMA_NAME_SUBJECTS = "subjects.json"
SDS_FILE_SAMPLES = "samples.xlsx"
SCHEMA_NAME_SAMPLES = "samples.json"
SDS_FILE_PERFORMANCES = "performances.xlsx"
SCHEMA_NAME_PERFORMANCES = "performances.json"
SDS_FILE_SITES = "sites.xlsx"
SCHEMA_NAME_SITES = "sites.json"