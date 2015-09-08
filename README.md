# Eve Genie

[![Documentation](https://readthedocs.org/projects/evegenie/badge/?version=latest)](http://evegenie.readthedocs.org/en/latest/) [![Build Status](https://travis-ci.org/newmediadenver/evegenie.svg?branch=master)](https://travis-ci.org/newmediadenver/evegenie) [![Coverage Status](https://coveralls.io/repos/newmediadenver/evegenie/badge.svg?branch=master&service=github)](https://coveralls.io/github/newmediadenver/evegenie?branch=master)

A tool for making [Eve](http://python-eve.org) schema generation easier.

**Use case**: You need to stand up an api quickly. You know what your data looks like in JSON but don't yet know the syntax for Eve/Cerberus.

## Docs

Documentation is within the [/docs directory](/docs/index.md) or online at [evegenie.readthedocs.org](http://evegenie.readthedocs.org/en/latest/)

## Requirements

    sudo pip install -r requirements.txt

## Example Usage

Create a json file, `sample.json`:

    {
      "sample-resource": {
        "sample-string": "asdf",
        "sample-integer": 42,
        "sample-float": 1.0,
        "sample-list": ["a", "b", "c"],
        "sample-dict": {
          "sample-embedded-list": ["a", "b", "c"],
          "sample-embedded-dict": {"sample-integer2": 20}
        }
      },
      "sample-resource2": {
        "sample-object-id": "objectid:sample-resource",
        "sample-intrange": "1-100",
        "sample-floatrange": "0.0-1.0"
      }
    }

Then generate your eve schemas using:

    python geneve.py sample.json

This will create a `sample.settings.py` file with the following contents:

    sample-resource = {
        'sample-list' : {
            'type' : 'list',
            'schema' : {
                'type' : 'string'
            }
        },
        'sample-integer' : {
            'type' : 'integer'
        },
        'sample-float' : {
            'type' : 'float'
        },
        'sample-dict' : {
            'type' : 'dict',
            'schema' : {
                'sample-embedded-list' : {
                    'type' : 'list',
                    'schema' : {
                        'type' : 'string'
                    }
                },
                'sample-embedded-dict' : {
                    'type' : 'dict',
                    'schema' : {
                        'sample-integer2' : {
                            'type' : 'integer'
                        }
                    }
                }
            }
        },
        'sample-string' : {
            'type' : 'string'
        }
    }
    
    sample-resource2 = {
        'sample-object-id' : {
            'type' : 'objectid',
            'data_relation' : {
                'field' : '_id',
                'resource' : 'sample-resource',
                'embeddable' : True
            }
        },
        'sample-intrange' : {
            'max' : 100,
            'type' : 'integer',
            'min' : 1
        },
        'sample-floatrange' : {
            'max' : 1.0,
            'type' : 'float',
            'min' : 0.0
        }
    }
    
    
    
    eve_settings = {
        'MONGO_HOST': 'localhost',
        'MONGO_DBNAME': 'testing',
        'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
        'BANDWIDTH_SAVER': False,
        'DOMAIN': {
            'sample-resource': sample-resource,
            'sample-resource2': sample-resource2,
        },
    }
