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

# import your data files and folders
sds.dataset.import(path='path/to/data')

# TODO: Add step where you set which high level folder a file gets assigned to


# map your imported data files to the entity structure defined in the SDS schema [here](sds_schema.py)
entity_structure = sds.get_entity_structure()

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
# set the submission metadata in the sds object. NOTE: Find definitions for the submission metadata in the SDS schema [here](sds_schema.py)
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
# import the generate module from the sds_create package
from sds_create import generate

# provide the Pennsieve API Key and secret
sds.upload.auth(api_key='api, api_secret='api_secret)

# upload new dataset 
# NOTE: You will need to download and start the Pennsieve Agent [here](https://app.pennsieve.io) to upload data to Pennsieve
dataset_id = generate(sds) # returns dataset_id

# OR upload to an existing pennsieve dataset
# set the generate options in the sds object
sds.set_generate_dataset_options(destination='existing-ps', if_existing="merge", if_existing_files="replace", dataset_id=dataset_id)
update_existing(sds)
```


## Utilities

### Compare a dataset on Pennsieve and a local dataset for differences 

```python
from sds_create import compare

# provide the Pennsieve API Key and secret
sds.upload.auth(api_key='api, api_secret='api_secret)

# import the dataset from Pennsieve 
sds.import_dataset(dataset_id='dataset_id')

# compare the Pennsieve dataset with the local dataset
results = compare(sds, local_dataset_location='path/to/local/dataset')
```