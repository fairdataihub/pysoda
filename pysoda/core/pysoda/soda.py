from soda_object import soda as soda_object

class Soda:
    def __init__(self, standard=""):
        self.soda_object = soda_object
        self.soda_object["standard"] = standard

    def set_standard(self, standard):
        self.soda_object["standard"] = standard

    def get_soda_object(self):
        return self.soda_object

    # Add more methods to alter the soda_object as needed
    def update_metadata(self, key, value):
        if key in self.soda_object["dataset-metadata"]:
            self.soda_object["dataset-metadata"][key] = value
        else:
            raise KeyError(f"{key} not found in dataset-metadata")

    def add_performance(self, performance):
        self.soda_object["performances"].append(performance)

    def add_subject_metadata(self, metadata):
        self.soda_object["subject-metadata"].append(metadata)

    def set_dataset_name(self, name):
        self.soda_object["dataset-metadata"]["name"] = name

    def get_dataset_name(self):
        return self.soda_object["dataset-metadata"]["name"]

    def get_submission(self):
        return self.soda_object["dataset-metadata"]["submission-metadata"]