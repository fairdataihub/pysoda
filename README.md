# sds-create

## Description

sds-create is a tool for your python workflows that can help you create SDS compliant datasets.

## Workflow

### Import the sds-create package into your project and intiialize the sds-create object

```python
from sds_create import sds_create
# initialize the sds-create object
# Internal note: sds_create returns the typical sodaJSONObj with additional methods for adding data and metadata [not in version 1]
# It is passed into the module functions just like our sodaJSONObj is passed to the backend of our api
sds = sds_create()

# add a dataset name to the sds object
sds.add_dataset_name('my_dataset')
```

### Structure your data

```python

# import your data files and folders and bucket them into the appropriate SDS category [ skippable, achieves the step of importing data into sodajsonobj in our front end code]
sds.dataset.import(path='path/to/data', category='category_name')


# create your sds entity structure that takes the below shape inside of the sds object:
# TODO: Create a validator for this structure in a separate python script
entity_structure = {
    'entity_name': {
        'entity_type': 'entity_type',
        'entity_category': 'entity_category',
        'entity_data': ['file_or_folder_path_1'], # include the path to the imported data TODO: Use ids or paths? ids may be easier to manage as then we only need to change the the path in once place if a file is moved
        'entity_children': {
            'entity_name': {
                'entity_type': 'entity_type',
                'entity_category': 'entity_category',
                'entity_data': ['file_or_folder_path_1'], # include the path to the imported data TODO: Use ids or paths? ids may be easier to manage as then we only need to change the the path in once place if a file is moved=,
                'entity_children': {
                    'entity_name': {
                        'entity_type': 'entity_type',
                        'entity_category': 'entity_category',
                        'entity_data': ['file_or_folder_path_1'], # include the path to the imported data TODO: Use ids or paths? ids may be easier to manage as then we only need to change the the path in once place if a file is moved
                        'entity_children': {}
                    }
                }
            }
        }
    }
}
entity_structure = sds.get_entity_structure()

# define the structure of the entity relationships as per the SDS schema

# set the entity structure in the sds object
sds.set_entity_structure(entity_structure)


```

### Create your dataset metadata

```python

# import the metadata module from the sds_create package
from sds_create import metadata

# define your submission metadata
submission = sds.get_submission_metadata()
......
# set the submission metadata in the sds object. NOTE: Find defnitions for the sub sructure here
sds.set_submission_metadata(submission)

# create the excel file for the submission metadata
metadata.submission.create(sds, file_output_location='path/to/output')


# repeat
metadata.subjects.create(sds, file_output_location='path/to/output')
metadata.samples.create(sds, file_output_location='path/to/output')
metadata.performances.create(sds, file_output_location='path/to/output')
metadata.sites.create(sds, file_output_location='path/to/output')
metadata.code.create(sds, file_output_location='path/to/output')
metadata.manifest.create(sds, file_output_location='path/to/output')

```

### Generate your dataset

```python
# provide the Pennsieve API Key and secret
sds.upload.auth(api_key='api, api_secret='api_secret)

# upload new dataset
sds.upload()

# upload to existing dataset
sds.upload(dataset_id='dataset_id', folders='merge or replace', files='replace or skip)


```
