# pysoda

## Description

pysoda is a tool for your python workflows that can help you create datasets in compliance with your favorite FAIR data standards.

## Workflow

### Import the pysoda package into your project and initialize the soda object with the supported standard of your choosing

```python
from pysoda import soda_create
# initialize the soda_create object
# Internal note: soda_create returns the typical sodaJSONObj with additional methods for adding data and metadata [not in version 1]
# It is passed into the module functions just like our sodaJSONObj is passed to the backend of our api

soda = soda_create(standard='sds')

# add a dataset name to the soda object
soda.set_dataset_name('my_dataset')

```

### Structure your data

```python


# get your base dataset files and folders structure
dataset_structure = soda.get_dataset_structure()

# fill out your dataset structure.
# NOTE: YOu will want to reference the
# dataset_structure key in the soda_schema.json file to understand the structure
# and what is required.
dataset_structure['folders'] = {'data': {'files': {}'file1': {}, 'file2': {}} 'folders': {'primary': {}}}
dataset_structure['files'] = {'filel1': {}} # NOTE: You can add metadata to the file here
dataset_structure['relativePath] = '/'


# map your imported data files to the entity structure defined in the soda schema [here](soda_schema.py)
entity_structure = soda.get_entity_structure()

# fill out your entity structure using the schema as a reference
# TODO: how are entities mapped to files in the schema?
enntity = {'subjectId': 'sub-1', 'metadata': {'age': '1 year', 'sex': 'female'}}
entity_structure['subjects'].append(entity)



```

### Create your dataset metadata

```python

# import the metadata module from the soda_create package
from soda_create import metadata

# define your submission metadata
submission = soda.get_submission_metadata()
......
# set the submission metadata in the soda object. NOTE: Find definitions for the submission metadata in the soda schema [here](soda_schema.py)
soda.set_submission_metadata(submission)

# create the excel file for the submission metadata
metadata.submission.create(soda, file_output_location='path/to/output')


# repeat
metadata.subjects.create(soda, file_output_location='path/to/output')
metadata.samples.create(soda, file_output_location='path/to/output')
metadata.performances.create(soda, file_output_location='path/to/output')
metadata.sites.create(soda, file_output_location='path/to/output')
metadata.code.create(soda, file_output_location='path/to/output')
metadata.manifest.create(soda, file_output_location='path/to/output')

```

### Generate your dataset

```python
# import the generate module from the soda_create package
from soda_create import generate

# provide the Pennsieve API Key and secret
soda.upload.auth(api_key='api, api_secret='api_secret)

# upload new dataset
# NOTE: You will need to download and start the Pennsieve Agent [here](https://app.pennsieve.io) to upload data to Pennsieve
dataset_id = generate(soda) # returns dataset_id

# OR upload to an existing pennsieve dataset
# set the generate options in the soda object
soda.set_generate_dataset_options(destination='existing-ps', if_existing="merge", if_existing_files="replace", dataset_id=dataset_id)
update_existing(soda)
```

## Utilities

### Compare a dataset on Pennsieve and a local dataset for differences

```python
from soda_create import compare

# provide the Pennsieve API Key and secret
soda.upload.auth(api_key='api, api_secret='api_secret)

# import the dataset from Pennsieve
soda.import_dataset(dataset_id='dataset_id')

# compare the Pennsieve dataset with the local dataset
results = compare(soda, local_dataset_location='path/to/local/dataset')
```
