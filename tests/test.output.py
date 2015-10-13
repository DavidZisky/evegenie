
user = {
    'schema': {
        'name': {
            'type': 'string'
        },
        'age': {
            'type': 'integer'
        },
        'experience': {
            'nullable': True
        },
        'alive': {
            'type': 'boolean'
        },
        'title': {
            'type': 'string'
        },
        'inventory': {
            'type': 'list',
            'schema': {
                'type': 'string'
            }
        },
        'primary_artifact': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'artifact',
                'field': '_id',
                'embeddable': True
            }
        },
        'secondary_artifacts': {
            'type': 'list',
            'schema': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'artifact',
                    'field': '_id',
                    'embeddable': True
                }
            }
        },
        'address': {
            'type': 'dict',
            'schema': {
                'address': {
                    'type': 'string'
                },
                'city': {
                    'type': 'string'
                },
                'state': {
                    'type': 'string'
                }
            }
        },
        'attack_bonus': {
            'type': 'integer',
            'min': 1,
            'max': 10
        },
        'difficulty': {
            'type': 'float',
            'min': 0.0,
            'max': 1.0
        },
        'attributes': {
            'allow_unknown': True
        }
    }
}

artifact = {
    'schema': {
        'name': {
            'type': 'string'
        },
        'cost': {
            'type': 'float'
        },
        'color': {
            'type': 'string'
        },
        'stats': {
            'type': 'dict',
            'schema': {
                'weight': {
                    'type': 'float'
                },
                'length': {
                    'type': 'float'
                },
                'powers': {
                    'type': 'dict',
                    'schema': {
                        'strike': {
                            'type': 'integer'
                        },
                        'deflect': {
                            'type': 'integer'
                        },
                        'speed': {
                            'type': 'integer'
                        },
                        'extra_powers': {
                            'allow_unknown': True
                        }
                    }
                }
            }
        }
    }
}

power_up = {
    'schema': {
        'name': {
            'type': 'string'
        }
    }
}



eve_settings = {
    'MONGO_HOST': 'localhost',
    'MONGO_DBNAME': 'testing',
    'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
    'BANDWIDTH_SAVER': False,
    'DOMAIN': {
        'user': user,
        'artifact': artifact,
        'power-up': power_up,
    },
}
