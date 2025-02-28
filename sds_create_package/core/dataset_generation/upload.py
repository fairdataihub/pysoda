import logging
from utils import (
    generate_options_set, generating_locally, generating_on_ps, 
    uploading_with_ps_account, uploading_to_existing_ps_dataset, 
    can_resume_prior_upload, virtual_dataset_empty, PropertyNotSetError, 
    connect_pennsieve_client, get_dataset_id, get_access_token,
    PennsieveActionNoPermission, PennsieveDatasetCannotBeFound,
    EmptyDatasetError
)
from permissions import pennsieve_get_current_user_permissions
from os.path import isdir

logger = logging.getLogger(__name__)

main_curate_progress_message = ""
main_curate_status = ""


def validate_dataset_structure(soda_json_structure, resume):

    global main_curate_status
    global main_curate_progress_message
    global logger

    # 1] Check for potential errors
    logger.info("main_curate_function step 1")

    if not generate_options_set(soda_json_structure):
        main_curate_status = "Done"
        raise PropertyNotSetError("generate-dataset") # used to be: abort(400, "Error: Please select an option to generate a dataset")

    # 1.1. If the dataset is being generated locally then check that the local destination is valid
    if generating_locally(soda_json_structure): 
        main_curate_progress_message = "Checking that the local destination selected for generating your dataset is valid"
        # TODO: Check for access errors too as that may be unclear for a package user
        if not valid_local_generation_path(soda_json_structure):
            main_curate_status = "Done"
            local_dataset_path = soda_json_structure["generate-dataset"]["path"]
            raise FileNotFoundError(f"Cannot find the local dataset path: {local_dataset_path}")
        

    logger.info("main_curate_function step 1.2")

    # 1.2. If generating dataset to Pennsieve or any other Pennsieve actions are requested check that the destination is valid
    if uploading_with_ps_account(soda_json_structure):
        # check that the Pennsieve account is valid
        try: 
            main_curate_progress_message = (
                "Checking that the selected Pennsieve account is valid"
            )
            accountname = soda_json_structure["bf-account-selected"]["account-name"]
            connect_pennsieve_client(accountname)
        except Exception as e:
            main_curate_status = "Done"
            raise e

 
    if uploading_to_existing_ps_dataset(soda_json_structure):
        # check that the Pennsieve dataset is valid
        try:
            main_curate_progress_message = (
                "Checking that the selected Pennsieve dataset is valid"
            )
            bfdataset = soda_json_structure["bf-dataset-selected"]["dataset-name"]
            selected_dataset_id = get_dataset_id(bfdataset)

        except Exception as e:
            main_curate_status = "Done"
            raise e

        # check that the user has permissions for uploading and modifying the dataset
        main_curate_progress_message = "Checking that you have required permissions for modifying the selected dataset"
        role = pennsieve_get_current_user_permissions(selected_dataset_id, get_access_token())["role"]
        if role not in ["owner", "manager", "editor"]:
            main_curate_status = "Done"
            PennsieveActionNoPermission(403, "Uploading to this dataset")

    logger.info("main_curate_function step 1.3")


    # 1.3. Check that specified dataset files and folders are valid (existing path) if generate dataset is requested
    # Note: Empty folders and 0 kb files will be removed without warning (a warning will be provided on the front end before starting the curate process)
    # Check at least one file or folder are added to the dataset
    main_curate_progress_message = "Checking that the dataset is not empty"
    if virtual_dataset_empty(soda_json_structure):
        main_curate_status = "Done" 
        EmptyDatasetError(soda_json_structure["generate-dataset"]["dataset-name"])
        # abort(400, "Error: Your dataset is empty. Please add valid files and non-empty folders to your dataset.")


    logger.info("main_curate_function step 1.3.1")

    # Check that local files/folders exist
    if error := check_local_dataset_files_validity(soda_json_structure):
        main_curate_status = "Done"
        abort(400, error)

    # check that dataset is not empty after removing all the empty files and folders
    if virtual_dataset_empty(soda_json_structure):
        main_curate_status = "Done"
        abort(400, "Error: Your dataset is empty. Please add valid files and non-empty folders to your dataset.")


    logger.info("main_curate_function step 1.3.2")
    # Check that bf files/folders exist (Only used for when generating from an existing Pennsieve dataset)
    if uploading_to_existing_ps_dataset(soda_json_structure) and can_resume_prior_upload(resume) == False:                     
        try:
            main_curate_progress_message = (
                "Checking that the Pennsieve files and folders are valid"
            )
            if soda_json_structure["generate-dataset"]["destination"] == "bf":
                if error := ps_check_dataset_files_validity(soda_json_structure):
                    logger.info("Failed to validate dataset files")
                    logger.info(error)
                    main_curate_status = "Done"
                    abort(400, error)
        except Exception as e:
            main_curate_status = "Done"
            raise e


def valid_local_generation_path(soda_json_structure):
    generate_dataset = soda_json_structure["generate-dataset"]
    local_dataset_path = generate_dataset["path"]
    return isdir(local_dataset_path)


def reset_upload_session_environment(resume):
    global main_curate_status
    global main_curate_progress_message
    global main_total_generate_dataset_size
    global main_generated_dataset_size
    global start_generate
    global generate_start_time
    global main_generate_destination
    global main_initial_bfdataset_size
    global main_curation_uploaded_files
    global uploaded_folder_counter
    global ums

    global myds
    global generated_dataset_id
    global bytes_file_path_dict
    global renaming_files_flow

    start_generate = 0
    myds = ""

    generate_start_time = time.time()

    # variables for tracking the progress of the curate process on the frontend 
    main_curate_status = ""
    main_curate_progress_message = "Starting..."
    main_total_generate_dataset_size = 0
    main_generated_dataset_size = 0
    main_curation_uploaded_files = 0
    uploaded_folder_counter = 0
    generated_dataset_id = None

    main_curate_status = "Curating"
    main_curate_progress_message = "Starting dataset curation"
    main_generate_destination = ""
    main_initial_bfdataset_size = 0

    if not resume:
        ums.set_df_mid(None)
        ums.set_elapsed_time(None)
        ums.set_total_files_to_upload(0)
        ums.set_main_total_generate_dataset_size(0)
        # reset the rename information back to default
        ums.set_renaming_files_flow(False) # this determines if we failed while renaming files after the upload is complete
        ums.set_rename_total_files(None)
        ums.set_list_of_files_to_rename(None)
        renaming_files_flow = False
        # reset the calculated values for the upload session
        bytes_file_path_dict = {}




def main_curate_function(soda_json_structure, resume):
    global logger
    global main_curate_status
    global manifest_id 
    global origin_manifest_id
    global total_files

    logger.info("Starting main_curate_function")
    logger.info(f"main_curate_function metadata generate-options={soda_json_structure['generate-dataset']}")
    start = timer()

    reset_upload_session_environment(resume)


    validate_dataset_structure(soda_json_structure, resume)

    
    logger.info("main_curate_function step 3")

    # 2] Generate
    main_curate_progress_message = "Generating dataset"
    try:
        if (soda_json_structure["generate-dataset"]["destination"] == "local"):
            logger.info("main_curate_function generating locally")
            generate_dataset(soda_json_structure, resume, ps=None)
        else:
            logger.info("main_curate_function generating on Pennsieve")
            accountname = soda_json_structure["bf-account-selected"]["account-name"]
            ps = connect_pennsieve_client(accountname)
            generate_dataset(soda_json_structure, resume, ps)
    except Exception as e:
        main_curate_status = "Done"
        raise e

    main_curate_status = "Done"
    main_curate_progress_message = "Success: COMPLETED!"
    end = timer()
    logger.info(f"Time for main_curate_function function: {timedelta(seconds=end - start)}")
    return {
        "main_curate_progress_message": main_curate_progress_message,
        "main_total_generate_dataset_size": main_total_generate_dataset_size,
        "main_curation_uploaded_files": main_curation_uploaded_files,
        "local_manifest_id": manifest_id,
        "origin_manifest_id": origin_manifest_id,
        "main_curation_total_files": total_files,
    }
