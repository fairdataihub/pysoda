# sds-create

## Description

sds-create is a tool for your python workflows that can help you create SDS compliant datasets.

## Workflow

### Import the sds-create package into your project and intiialize the sds-create object

```python
from sds_create import sds_create
# initialize the sds-create object
sds = sds_create()

# initialize a new dataset
sds.create_dataset('my_dataset')
```

### Structure your data

```python

# import your data files and folders and bucket them into the appropriate SDS category
sds.dataset.data.import(path='path/to/data', category='category_name')


# import your SDS entity structure and create the entity mappings to the data files and folders
# TODO: Create a validator for this structure in a separate python script
# TODO: Make clear that there is a 'sodaJSONObj' we create for you that is used as input to the python module methods
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
sds.entities.import(entity_structure)


```

### Create your dataset metadata

```python

# TODO: Define metadata structure that is used within the sds_struct object for submission files
# TODO: Methods for creating the metadata sub structures within the sds_struct for the metadata files
sds.metadata.submission.create(sds_struct)
sds.metadata.subjects.create(sds_struct)
sds.metadata.samples.create(sds_struct)
sds.metadata.performances.create(sds_struct)
sds.metadata.sites.create(sds_struct)
sds.metadata.code.create(sds_struct)
sds.metadata.manifest.create(sds_struct)

```

### Generate your dataset

#### Generating the dataset locally

#### Generating the dataset on Pennsieve [new]

#### Generating the dataset on Pennsieve [updating existing]
