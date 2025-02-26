import jsonschema
from jsonschema import validate



sds_schema = {
    "type": "object",
    "properties": {
      "starting-point": {
        "type": "object",
        "properties": {
          "origin": {
            "type": "string", 
            "enum": ["ps", "local", "new"]
          },
        },
      },
      "ps-dataset-selected": {
        "type": "object",
        "properties": {
          "dataset-name": {"type": "string"}
        },
      },
      "ps-account-selected": {
        "type": "object",
        "properties": {
          "account-name": {"type": "string"}
        }
      },
      "guided-manifest-file-data": {
        "type": "object",
        "properties": {
          "headers": {"type": "string"}, # TODO: Define how?
          "data": {"type": "string"}, # TODO: Define how?
        }
      },
      "dataset-validated": {
        "type": "boolean"
      },
      "dataset-validation-errors": {
        "type": "array",
        "items": {"type": "string"}
      },

      "dataset-structure": {
        "type": "object", 
        "properties": {
          "folders": {
            "type": "object",
            "properties": {
              "folder-name": {"type": "string"},
              "folders": {
                "$ref": "#/properties/dataset-structure/properties/folders"
              },
              "files": {
                "type": "object",
                "patternProperties": {
                    ".*": {  # Matches any file name
                        "type": "object",
                        "properties": {
                            "timestamp": {"type": "string"},
                            "size": {"type": "number"},
                            "checksum": {"type": "string"},
                            "description": {"type": "string"},
                            "additional-metadata": {"type": "string"}, #TODO: Define how?
                            "extra-columns": {"type": "string"} #TODO: Define how?

                        },
                        "required": ["timestamp", "size", "checksum"]
                    }
                },
                "additionalProperties": False
              },
            },
          },
          "files": {
            "type": "object",
            "patternProperties": {
                ".*": {  # Matches any file name
                    "type": "object",
                    "properties": {
                        "timestamp": {"type": "string"},
                        "size": {"type": "number"},
                        "checksum": {"type": "string"}
                    },
                    "required": ["timestamp", "size", "checksum"]
                }
            },
            "additionalProperties": False
          },
        }, 
      },

      "dataset-metadata": {
        "type": "object",
        "properties": {
          "description-metadata": {
            "type": "object",
            "properties": {
              "description": {
                "type": "object",
                "properties": {
                  "study-purpose": {"type": "string"},
                  "data-collectoin": {"type": "string"},
                  "primary-conclusion": {"type": "string"},
                }
              },
              "additional-links": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "link": {"type": "string"},
                    "relation": {"type": "string"},
                    "description": {"type": "string"},
                    "linkType": {"type": "string"},
                    "isFair": {"type": "boolean"},
                  }
                }
              }, #TODO: Define how?
              "contributors": {
                "type": "object",
                "properties": {
                  "conID": {"type": "string"},
                  "conAffiliation": {"type": "string"},
                  "conName": {"type": "string"},
                  "conRole": {"type": "string"},
                  "contributorFirstName": {"type": "string"},
                  "contributorLastName": {"type": "string"},
                }
              },
              "contributor-information": {
                 "type": "object",
                 "properties": {
                   "funding": {"type": "array", "items": {"type": "string"}},
                   "acknowledgment": {"type": "string"},
                 }
               }, #TODO: Define how?
              "protocols": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "link": {"type": "string"},
                    "tyype": {"type": "string"},
                    "relation": "IsProtocolFor",
                    "description": {"type": "string"},
                    "additional-metadata": {"type": "boolean"}
                  }
                }
              },
              "dataset-information": {
                "type": "object",
                "properties": {
                  "name": {"type": "string"},
                  "description": {"type": "string"},
                  "studyType": {"type": "string"},
                  "keywords": {"type": "array", "items": {"type": "string"}},
                  "number of samples": {"type": "number"},
                  "number of subjects": {"type": "number"},
                  "study organ system": {"type": "array", "items": {"type": "string"}},
                  "study approach": {"type": "array", "items": {"type": "string"}},
                  "study technique": {"type": "array", "items": {"type": "string"}},
                  "study purpose": {"type": "string"},
                  "study data collection": {"type": "string"},
                  "study primary conclusion": {"type": "string"},
                  "study collection title": {"type": "string"},
                }
              },
              "study-information": {
                "type": "object",
                "properties": {
                  "study purpose": {"type": "string"},
                  "study data collection": {"type": "string"},
                  "study primary conclusion": {"type": "string"},
                }
              },
            }
          },
          "shared-metadata":  {
            "type": "object"
          },
          "protocol-data": {
            "type": "array"
          },
          "subject-metadata": {
            "type": "object"
          },
          "sample-metadata": {
            "type": "object"
          },
          "submission-metadata": {
            "type": "object"
          },
          "code-metadata": {
            "type": "object"
          },
          "README": {
            "type": "string"
          },
          "CHANGES": {
            "type": "string"
          },
        }
      },
      "digital-metadata": {
        "type": "object",
        "properties": {
          "description": {"type": "object"},
          "pi-owner": {"type": "object"},
          "user-permissions": {"type": "array"},
          "team-permissions": {"type": "array"},
          "license": {"type": "string"},
          "name": {"type": "string"},
        }
      },
      "generate-dataset": {
        "type": "object",
        "properties": {
          "destination": {"type": "string", "enum": ["ps", "local"]},
          "if-existing": {"type": "string", "enum": ["replace", "skip", "merge"]},
          "if-existing-files": {"type": "string", "enum": ["replace", "skip"]},
          "generate-option": {"type": "string", "enum": ["new", "existing-ps"]},
          "path": {"type": "string"},
          "dataset-name": {"type": "string"},
        }
      },
      



    }
}