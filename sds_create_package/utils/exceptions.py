
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
    

class EmptyDatasetError(Exception):
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.error_message = f"The dataset {self.dataset_name} is empty."

    def __str__(self):
        return self.error_message