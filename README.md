# Eve Genie

![last_commit](https://img.shields.io/github/last-commit/DavidZisky/evegenie)
![](https://github.com/DavidZisky/evegenie/workflows/evegenie_build/badge.svg)

Evegenie is a tool for making [Eve](http://python-eve.org) schema generation easier. By providing JSON file with data and executing single command it can generate whole settings.py file for your Python Eve application. Originally developed by [@drud](https://github.com/drud)

Latest Eve version tested: 1.1.5

Python Eve (by default) uses MongoDB as a database. The easiest way for quick development with MongoDB is to sping up a MongoDB container by executing:

```bash
docker run --name mongodb -p 27017:27017 -d mongo
```

## Requirements

```bash
pip install -r requirements.txt
```
    
 You should install Python Eve yourself (not included in requirements)
```bash
pip install eve
```

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
## Special evegenie strings

Certain strings passed in via the source json will be converted to eve schema types with sane defaults.

- `"fieldname": "objectid:sample-entity"` will add data_relation to sample-entity to the schema
- `"fieldname": "0-100"` will create an integer with a min of 0 and a max of 100
- `"fieldname": "0.0-1.0"` will create a float with a min of 0 and a max of 1
- `"fieldname": {"allow_unknown": true}` will translate directly to fieldname that allows the unknown
