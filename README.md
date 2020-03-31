# Eve Genie

![](https://img.shields.io/github/last-commit/DavidZisky/evegenie) [![Documentation](https://readthedocs.org/projects/evegenie/badge/?version=latest)](http://evegenie.readthedocs.org/en/latest/) ![](https://github.com/DavidZisky/evegenie/workflows/evegenie_build/badge.svg)

Evegenie is a tool for making [Eve](http://python-eve.org) schema generation easier. By providing JSON file with data and executing single command it can generate whole settings.py file for your Python Eve application. Originally developed by [@drud](https://github.com/drud)

Latest Eve version tested: 1.0

## Docs

Documentation is within the [/docs directory](/docs/index.md)

## Requirements

    sudo pip install -r requirements.txt

## Example Usage

Create a json file, `sample.json`. 

```javascript
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
    "sample-floatrange": "0.0-1.0",
    "sample-unknown": {
      "allow_unknown": true
    }
  }
}
```

Then generate your eve schemas using:

```bash
python3 geneve.py sample.json
```

This will create a `sample.settings.py` file. Change it's name to settings.py and you can simply run the API with:
```bash
python3 run.py
```

Geneve created file with the following contents which is used by Python Eve as a settings file:

```python
import os

MONGO_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/evegenie')

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']


sample_resource = {
    'schema': {
        'sample-string': {
            'type': 'string'
        },
        'sample-integer': {
            'type': 'integer'
        },
        'sample-float': {
            'type': 'float'
        },
        'sample-list': {
            'type': 'list',
            'schema': {
                'type': 'string'
            }
        },
        'sample-dict': {
            'type': 'dict',
            'schema': {
                'sample-embedded-list': {
                    'type': 'list',
                    'schema': {
                        'type': 'string'
                    }
                },
                'sample-embedded-dict': {
                    'type': 'dict',
                    'schema': {
                        'sample-integer2': {
                            'type': 'integer'
                        }
                    }
                }
            }
        }
    }
}

sample_resource2 = {
    'schema': {
        'sample-object-id': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'sample-resource',
                'field': '_id',
                'embeddable': True
            }
        },
        'sample-intrange': {
            'type': 'integer',
            'min': 1,
            'max': 100
        },
        'sample-floatrange': {
            'type': 'float',
            'min': 0.0,
            'max': 1.0
        },
        'sample-unknown': {
            'allow_unknown': True
        }
    }
}



DOMAIN = {
        'sample-resource': sample_resource,
        'sample-resource2': sample_resource2,
}

```
