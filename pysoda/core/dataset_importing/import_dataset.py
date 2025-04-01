import logging
import os
import requests

from ...constants import PENNSIEVE_URL
from ...utils import create_request_headers, get_access_token, get_dataset_id, PennsieveActionNoPermission
from ..permissions import pennsieve_get_current_user_permissions
from ..metadata import load_metadata_to_dataframe

logger = logging.getLogger(__name__)


def import_pennsieve_dataset(soda_json_structure, requested_sparc_only=True):
    global logger
    high_level_sparc_folders = [
        "code",
        "derivative",
        "docs",
        "primary",
        "protocol",
        "source",
    ]
    manifest_sparc = ["manifest.xlsx", "manifest.csv"]
    high_level_metadata_sparc = [
        "submission.xlsx",
        "submission.csv",
        "submission.json",
        "dataset_description.xlsx",
        "dataset_description.csv",
        "dataset_description.json",
        "subjects.xlsx",
        "subjects.csv",
        "subjects.json",
        "samples.xlsx",
        "samples.csv",
        "samples.json",
        "README.txt",
        "CHANGES.txt",
        "code_description.xlsx",
        "inputs_metadata.xlsx",
        "outputs_metadata.xlsx",
    ]
    double_extensions = [
        ".ome.tiff",
        ".ome.tif",
        ".ome.tf2,",
        ".ome.tf8",
        ".ome.btf",
        ".ome.xml",
        ".brukertiff.gz",
        ".mefd.gz",
        ".moberg.gz",
        ".nii.gz",
        ".mgh.gz",
        ".tar.gz",
        ".bcl.gz",
    ]

    global create_soda_json_completed
    global create_soda_json_total_items
    global create_soda_json_progress
    create_soda_json_progress = 0
    create_soda_json_total_items = 0
    create_soda_json_completed = 0

    # ["extensions"] doesn't seem to be returned by the Pennsieve API anymore
    def verify_file_name(file_name, extension):
        global logger
        if extension == "":
            return file_name

        double_ext = False
        for ext in double_extensions:
            if file_name.find(ext) != -1:
                double_ext = True
                break
                
        extension_from_name = ""

        if double_ext == False:
            extension_from_name = os.path.splitext(file_name)[1]
        else:
            extension_from_name = (
                os.path.splitext(os.path.splitext(file_name)[0])[1]
                + os.path.splitext(file_name)[1]
            )

        if extension_from_name == ("." + extension):
            return file_name
        else:
            return file_name + ("." + extension)


    def createFolderStructure(subfolder_json, manifest):
        """
            Function for creating the Pennsieve folder structure for a given dataset as an object stored locally.
            Arguments:
                subfolder_json: The json object containing the folder structure of the dataset
                pennsieve_client: The Pennsieve client object
                manifest: The manifest object for the dataset
        """
        # root level folder will pass subfolders into this function and will recursively check if there are subfolders while creating the json structure
        global logger
        global create_soda_json_progress
        
        collection_id = subfolder_json["path"]

        limit = 100
        offset = 0
        subfolder = []
        while True: 
            r = requests.get(f"{PENNSIEVE_URL}/packages/{collection_id}?limit={limit}&offset={offset}", headers=create_request_headers(get_access_token()))
            r.raise_for_status()
            page = r.json()["children"]
            subfolder.extend(page)
            if len(page) < limit:
                break
            offset += limit

        for items in subfolder:
            folder_item_name = items["content"]["name"]
            create_soda_json_progress += 1
            item_id = items["content"]["id"]
            # is a file name check if there are additional manifest information to attach to files
            if item_id[2:9] == "package":
                if (
                    folder_item_name[0:8] != "manifest"
                ):  # manifest files are not being included in json structure

                    # verify file name first (used for legacy Pennsieve datasets)
                    if("extension" not in subfolder):
                        folder_item_name = verify_file_name(folder_item_name, "")
                    else:
                        folder_item_name = verify_file_name(folder_item_name, subfolder["extension"])
                        
                    # verify timestamps
                    timestamp = items["content"]["createdAt"].replace('.', ',')

                    paths_list = [*subfolder_json["bfpath"]]
                    subfolder_json["files"][folder_item_name] = {
                        "action": ["existing"],
                        "path": item_id,
                        "bfpath": paths_list,
                        "timestamp": timestamp,
                        "type": "bf",
                        "additional-metadata": "",
                        "description": "",
                    }
                    
                    # creates path for folder_item_name (stored in temp_name)
                    if len(subfolder_json["files"][folder_item_name]["bfpath"]) > 1:
                        temp_name = '/'.join(subfolder_json["files"][folder_item_name]["bfpath"][1:]) + "/" + folder_item_name
                    else:
                        temp_name = folder_item_name
                    
                    if len(manifest.keys()) > 0:
                        # Dictionary that has the required manifest headers in lowercase and without spaces as keys
                        # and the correct manifest headers as values
                        defaultManifestHeadersNameMapped = {
                            "filename": "filename",
                            "timestamp": "timestamp",
                            "description": "description",
                            "filetype": "file type",
                            "additionalmetadata": "additional-metadata",
                        }

                        # Dictionary that will be used to store the correct manifest headers as keys
                        # and the values from the manifest as values
                        updated_manifest = {}

                        # Go through the imported manifest keys and change the keys to the correct name
                        # For example if the key is "File Name" change it to "filename"
                        for manifestKey in manifest.keys():
                            # Make the key lowercase
                            sterilizedKeyName = manifestKey.lower().replace(" ", "")
                            if sterilizedKeyName in defaultManifestHeadersNameMapped.keys():
                                # change the key to the correct name
                                # For example if the key name is "filetype" change it to "file type"
                                newManifestKeyName = defaultManifestHeadersNameMapped[sterilizedKeyName]
                                # Add the new key/value to the updated manifest
                                updated_manifest[newManifestKeyName] = manifest[manifestKey]
                            else:
                                # Keep the key/value the same and add it to the updated manifest
                                updated_manifest[manifestKey] = manifest[manifestKey]

                        if "filename" in updated_manifest.keys():
                            for manifestKey in updated_manifest.keys():
                                location_index = ""
                                # get the index of the file name in the manifest
                                if (temp_name in updated_manifest["filename"].values()):
                                    location_index = list(updated_manifest["filename"].values()).index(
                                        temp_name
                                    )
                                # This is for the case where the file name in the manifest has a slash at the beginning
                                # which is the case for files in the root folder
                                elif ("/" + temp_name in updated_manifest["filename"].values()):
                                    location_index = list(updated_manifest["filename"].values()).index(
                                        "/" + temp_name
                                    )
                                else:
                                    # break out of the for loop if the file name is not in the manifest
                                    break

                                # check if the key is in the required manifest headers, if it is, update the folder_item_name value
                                # corresponding to the key
                                if manifestKey in defaultManifestHeadersNameMapped.values():
                                    if updated_manifest[manifestKey][location_index] != "":
                                        if folder_item_name[0:1] == "/":
                                            subfolder_json["files"][folder_item_name[:1]][manifestKey] = updated_manifest[manifestKey][location_index]
                                        else:
                                            subfolder_json["files"][folder_item_name][manifestKey] = updated_manifest[manifestKey][location_index]
                                # if the key is not in the required manifest headers, add it to the extra columns folder_item_name value
                                else :
                                    # if the extra columns key does not exist, create it
                                    if "extra_columns" not in subfolder_json["files"][folder_item_name]:
                                        subfolder_json["files"][folder_item_name]["extra_columns"] = {}
                                    
                                    if updated_manifest[manifestKey][location_index] != "":
                                        subfolder_json["files"][folder_item_name]["extra_columns"][manifestKey] = updated_manifest[manifestKey][location_index]
                                    else:
                                        subfolder_json["files"][folder_item_name]["extra_columns"][manifestKey] = ""
                        else:
                            # filename not in updated manifest so recreate standard headers if they don't exist
                            # loop through the updated manifest keys and if header matches standard header add content else recreate
                            if len(updated_manifest.keys()) > 0:
                                location_index = ""
                                for manifestKey in updated_manifest.keys():
                                    if temp_name in updated_manifest[manifestKey].values():
                                        # file_names found
                                        location_index = list(updated_manifest[manifestKey].values()).index(
                                        temp_name
                                        )
                                    if ("/" + temp_name in updated_manifest[manifestKey].values()):
                                        location_index = list(updated_manifest[manifestKey].values()).index(
                                        "/" + temp_name
                                        )
                                    if location_index != "":
                                        if manifestKey in defaultManifestHeadersNameMapped.values():
                                            if folder_item_name[0:1] == "/":
                                                subfolder_json["files"][folder_item_name[1:]][manifestKey] = updated_manifest[manifestKey][location_index]
                                            else:
                                                subfolder_json["files"][folder_item_name][manifestKey] = updated_manifest[manifestKey][location_index]
                                        else:
                                            if "extra_columns" not in subfolder_json["files"][folder_item_name]:
                                                subfolder_json["files"][folder_item_name]["extra_columns"] = {}
                                            subfolder_json["files"][folder_item_name]["extra_columns"][manifestKey] = updated_manifest[manifestKey][location_index]

            else:  # another subfolder found
                paths_list = [*subfolder_json["bfpath"], folder_item_name]
                subfolder_json["folders"][folder_item_name] = {
                    "action": ["existing"],
                    "path": item_id,
                    "bfpath": paths_list,
                    "files": {},
                    "folders": {},
                    "type": "bf",
                }

        if len(subfolder_json["folders"].keys()) != 0:  # there are subfolders
            for folder in subfolder_json["folders"].keys():
                subfolder = subfolder_json["folders"][folder]
                createFolderStructure(subfolder, manifest)


    # check that the Pennsieve dataset is valid
    try:
        bf_dataset_name = soda_json_structure["bf-dataset-selected"]["dataset-name"]
    except Exception as e:
        raise e

    selected_dataset_id = get_dataset_id(bf_dataset_name)

    # check that the user has permission to edit this dataset
    role = pennsieve_get_current_user_permissions(selected_dataset_id, get_access_token())["role"]
    if role not in ["owner", "manager", "editor"]:
        curatestatus = "Done"
        raise PennsieveActionNoPermission("You do not have permissions to edit upload this Pennsieve dataset.")


    # surface layer of dataset is pulled. then go through through the children to get information on subfolders
    manifest_dict = {}
    manifest_error_message = []
    soda_json_structure["dataset-structure"] = {
        "files": {},
        "folders": {},
    }

    # root of dataset is pulled here (high level folders/files are gathered here)
    # root_folder is the files and folders within root
    r = requests.get(f"{PENNSIEVE_URL}/datasets/{selected_dataset_id}", headers=create_request_headers(get_access_token()))
    r.raise_for_status()
    root_folder = r.json()["children"]

    # Get the amount of files/folders in the dataset
    r = requests.get(f"{PENNSIEVE_URL}/datasets/{selected_dataset_id}/packageTypeCounts", headers=create_request_headers(get_access_token()))
    r.raise_for_status()
    packages_list = r.json()


    # root's children files
    for count in packages_list.values():
        create_soda_json_total_items += int(count)

    # Go through the content in the root folder
    for items in root_folder:
        item_id = items["content"]["id"]
        item_name = items["content"]["name"]
        # If package type is Collection, then it is a folder
        if items["content"]["packageType"] == "Collection" and item_name in high_level_sparc_folders:
            create_soda_json_progress += 1
            soda_json_structure["dataset-structure"]["folders"][item_name] = {
                "type": "bf",
                "path": item_id,
                "action": ["existing"],
                "files": {},
                "folders": {},
                "bfpath": [item_name],
            }

            manifest_dict[item_name] = {}
            # Check the content of the folder to see if a manifest file exists
            r = requests.get(f"{PENNSIEVE_URL}/packages/{item_id}", headers=create_request_headers(get_access_token()))
            r.raise_for_status()
            folder_content = r.json()["children"]

            if len(folder_content) > 0:
                for package in folder_content:
                    package_name = package["content"]["name"]
                    if package_name in manifest_sparc:
                        # item is manifest
                        df = ""
                        package_id = package["content"]["id"]
                        try:                            
                            if package_name.lower() == "manifest.xlsx":
                                df = load_metadata_to_dataframe(package_id, "excel", get_access_token())
                                df = df.fillna("")
                            else:
                                df = load_metadata_to_dataframe(package_id, "csv", get_access_token())
                                df = df.fillna("")
                            manifest_dict[item_name].update(df.to_dict())
                        except Exception as e:
                            manifest_error_message.append(
                                items["content"]["name"]
                            )

                high_lvl_folder_dict = soda_json_structure["dataset-structure"]["folders"][
                    item_name
                ]

                if item_name in manifest_dict:
                    createFolderStructure(
                        high_lvl_folder_dict, manifest_dict[item_name]
                    )  # passing item's json and the collection ID


        else:
            # Item is a metadata file
            if item_name in high_level_metadata_sparc:
                create_soda_json_progress += 1
                if "metadata-files" in soda_json_structure.keys():
                    soda_json_structure["metadata-files"][item_name] = {
                        "type": "bf",
                        "action": ["existing"],
                        "path": item_id,
                    }

    success_message = (
        "Data files under a valid high-level SPARC folders have been imported"
    )
    create_soda_json_completed = 1

    logger.info(f"Time to import {soda_json_structure['bf-dataset-selected']['dataset-name']} ")
    return {
        "soda_object": soda_json_structure,
        "success_message": success_message,
        "manifest_error_message": manifest_error_message,
        "import_progress": create_soda_json_progress,
        "import_total_items": create_soda_json_total_items,
    }
