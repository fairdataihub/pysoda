
# create a custom exception that indicates a property in an object has not been set
class PropertyNotSetError(Exception):
    def __init__(self, property_name):
        self.property_name = property_name
        self.error_message = f"The property {self.property_name} has not been set."

    def __str__(self):
        return self.error_message
    

# create a custom exception that indicates that the 'PennsieveAgent' could not be started
class PennsieveAgentError(Exception):
    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return self.error_message
    
class FailedToFetchPennsieveDatasets(Exception):
    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return self.error_message
    
class PennsieveDatasetCannotBeFound(Exception):
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.error_message = f"The Pennsie dataset {self.dataset_name} could not be found."

    def __str__(self):
        return self.error_message
    
    
class ConfigProfileNotSet(Exception):
    def __init__(self, profile_name):
        self.profile_name = profile_name
        self.error_message = f"The profile {self.profile_name} has not been set."

    def __str__(self):
        return self.error_message
    

class PennsieveActionNoPermission(Exception):
    def __init__(self, action):
        self.action = action
        self.error_message = f"Do not have the correct permissions to perform action: {self.action} ."

    def __str__(self):
        return self.error_message

class GenericUploadError(Exception):
    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return self.error_message
    

class EmptyDatasetError(Exception):
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.error_message = f"The dataset {self.dataset_name} is empty."

    def __str__(self):
        return self.error_message
    

class LocalDatasetMissingSpecifiedFiles(Exception):
    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return self.error_message


    

def validation_error_message(e):
    """
    Print a message for a validation error.
    input: e (ValidationError): The validation error from the validate library.
    output: human readable message for the validation error.
    """
    msg = "There following error was found in your metadata:"
    e_type = e.schema_path.pop().strip()
    print(e.schema_path)
    if e_type == "type":
        s = ''
        while e.schema_path:
            p_v = e.schema_path.popleft()
            if p_v.strip() != "properties":
                if s != '':
                    s += ' -> '
                s += p_v
        msg = f"{msg} {s} needs to be a list of values."
    if e_type == "required":
        # peel out the first line from the stringified error message
        msg = f"{msg} {e.message.splitlines()[0]}"
    return msg