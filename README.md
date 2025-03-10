# pysoda

## Overview

Pysoda is a tool for your python workflows that can help you create datasets in compliance with your favorite FAIR(Findable, Accessible, Interoperable, Reusable) data standards. At the moment, pysoda is primarily focused on neuromodulation, neurophysiology, and related data according to the SPARC guidelines that are aimed at making data FAIR. However, we are envisioning to extend the tool to support other standards such as BIDS, FHIR, etc, in the future.

Pysoda stems from SODA, a desktop software that simplifies the organization and sharing of data that needs to comply to a FAIR data standard. While using the SODA app can be convenient for most investigators, others with coding proficiency may find it more convenient to implement automated workflows. Given that the backend of SODA contains many functions necessary for preparing and submitting a dataset that is compliant with the SPARC Data Structure (SDS) such as:

Creating standard metadata files
Generating manifest files
Automatically complying with the file/folder naming conventions
Validating against the offical SDS validator
Uploading dataset to Pennsieve with SDS compliance (ignoring empty folders and non-allowed files, avoiding duplicate files and folders, etc.)
And many more

Pysoda makes these functions, which have been thoroughtly tested and validated, easily integratable in automated workflows such that the investigators do not have to re-write them. This will be very similar to the [pyfairdatatools](https://github.com/AI-READI/pyfairdatatools) Python package we are developing for our [AI-READI](https://aireadi.org/) project as part of the NIH Bridge2AI program.

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
dataset_structure['folders'] = {
    'data': {
        'files': {
            'file1': {
                'path': '/home/user/file1.txt', 'relativePath': '/data/file1.txt', 'action': 'new'
            }, 
            'file2': {
                'path': '/home/user/file2.txt', 'relativePath': '/data/file2.txt', 'action': 'new'
            }
        }, 
        'folders': {
            'primary': {
                'files': {
                    'file3': {
                        'path': '/home/user/file3.txt', 'relativePath': '/data/primary/file3.txt', 'action': 'new'
                    }
                }
            }
        },
        'relativePath': '/data'
    },
    'files': {},
    'relativePath': '/'
}


# map your imported data files to the entity structure defined in the soda schema [here](soda_schema.py)
entity_structure = soda.get_entity_structure()

# fill out your entity structure using the schema as a reference
# NOTE: data model not finalized
entity = {'subjectId': 'sub-1', 'metadata': {'age': '1 year', 'sex': 'female'}, 'data-file': '/data/file1.txt'}
entity_structure['subjects'].append(entity)



```

### Create your dataset metadata

```python

# import the metadata module from the soda_create package
from pysoda import metadata

# define your submission metadata
submission = soda.get_submission_metadata()

submission['consortium-data-standard'] = 'standard'
submission['funding-consortium'] = 'SPARC'
submission['award-number'] = '12345'
submission['milestone-acheieved'] = ['one', 'two', 'three']
submission['filepath'] = 'path/to/destination'

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

#### Generate locally

```python

from pysoda import generate

# set the generation options
soda.set_generate_dataset_options(destination='local', path='path/to/destination', dataset_name='my_dataset')

# generate the dataset
generate(soda)

```

#### Generate on Pennsieve

```python
from pysoda import generate

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
from pysoda import compare

# provide the Pennsieve API Key and secret
soda.upload.auth(api_key='api, api_secret='api_secret)

# import the dataset from Pennsieve
soda.import_dataset(dataset_id='dataset_id')

# compare the Pennsieve dataset with the local dataset
results = compare(soda, local_dataset_location='path/to/local/dataset')
```
