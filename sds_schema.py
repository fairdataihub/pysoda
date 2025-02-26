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
              "patternProperties": {
                ".*": { # match any folder name
                  "type": "object",
                  "properties": {
                    "folders": {
                      "$ref": "#/properties/dataset-structure/properties/folders"
                    },
                    "files": {
                      "type": "object",
                      "properties": {
                        "patternProperties": {
                            ".*": {  # Matches any file name
                                "type": "object",
                                "properties": {
                                    "timestamp": {"type": "string"},
                                    "size": {"type": "number"},
                                    "checksum": {"type": "string"},
                                    "description": {"type": "string"},
                                    "additional-metadata": {"type": "string"}, #TODO: Define how?
                                    "extra-columns": {"type": "string"}, #TODO: Define how?
                                    "extension": {"type": "string"},
                                    "action": {
                                      "type": "array", 
                                      "items": {
                                        "type": "string"
                                      }
                                    },
                                    "relativePath": {
                                      "type": "string"
                                    },
                                    "path": {
                                      "type": "string"
                                    }, 
                                    "location": {"type": "string", "enum": ["local", "pennsieve"]},
                                },
                                "required": ["timestamp", "size", "checksum"]
                            }
                        },
                        "additionalProperties": False
                      }
                    }
                  },
                },
              },
              "action": {
                "type": "array", 
                "items": {
                  "type": "string"
                }
              },
              "relativePath": {
                "type": "string"
              },
              "path": {
                "type": "string"
              }, 
              "location": {"type": "string", "enum": ["local", "pennsieve"]}, 
            
          },
          "files": {
            "type": "object",
            "properties": {
              "patternProperties": {
                  ".*": {  # Matches any file name
                      "type": "object",
                      "properties": {
                          "timestamp": {"type": "string"},
                          "size": {"type": "number"},
                          "checksum": {"type": "string"},
                          "description": {"type": "string"},
                          "additional-metadata": {"type": "string"}, #TODO: Define how?
                          "extra-columns": {"type": "string"}, #TODO: Define how?
                          "extension": {"type": "string"},
                          "action": {
                            "type": "array", 
                            "items": {
                              "type": "string"
                            }
                          },
                          "relativePath": {
                            "type": "string"
                          },
                          "path": {
                            "type": "string"
                          }, 
                          "location": {"type": "string", "enum": ["local", "pennsieve"]},
                      },
                      "required": ["timestamp", "size", "checksum"]
                  }
              },
              "additionalProperties": False
            }
          },
          "relativePath": {
            "type": "string"
          },
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
                    "relation": {"type": "string"},
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
      "dataset-entity-structure": {
        "type": "object",
        "properties": {
          "subjects": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "subjectId": {"type": "string"},
                "metadata": {"type": "object"},
                "samples": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "sampleId": {"type": "string"},
                      "metadata": {"type": "object"},
                    }
                  }
                }
              }
            },
          },
        }
      },
      "dataset-entity-obj": {
        "type": "object",
        "properties": {
          "bucketed-data": {
            "type": "object",
            "properties": {
              "code": {"type": "array", "items": {"type": "string", "format": "file-path"}},
              "experimental-data": {"type": "array", "items": {"type": "string", "format": "file-path"}},
              "other": {"type": "array", "items": {"type": "string", "format": "file-path"}},
            }
          }
        }
      }
    }
}


sds_e = {
  "dataset-structure": {
    "folders": {
      "root-folder": {
        "folders": {
          "nested-folder": {
            "files": {
              "file1.txt": {
                "timestamp": "2023-01-01T00:00:00Z",
                "size": 1234,
                "checksum": "abc123",
                "description": "Test file 1",
                "additional-metadata": "metadata1",
                "extra-columns": "extra1"
              },
              "file2.txt": {
                "timestamp": "2023-01-02T00:00:00Z",
                "size": 5678,
                "checksum": "def456",
                "description": "Test file 2",
                "additional-metadata": "metadata2",
                "extra-columns": "extra2"
              }
            }
          },
          "other-nested-folder": {
            "files": {
              "file3.txt": {
                "timestamp": "2023-01-03T00:00:00Z",
                "size": 91011,
                "checksum": "ghi789",
                "description": "Test file 3",
                "additional-metadata": "metadata3",
                "extra-columns": "extra3"
              }
            }
          }
        },
        "files": {
          "file3.txt": {
            "timestamp": "2023-01-03T00:00:00Z",
            "size": 91011,
            "checksum": "ghi789",
            "description": "Test file 3",
            "additional-metadata": "metadata3",
            "extra-columns": "extra3"
          }
        }
      }
    }
  }
}

validate(sds_e, sds_schema)