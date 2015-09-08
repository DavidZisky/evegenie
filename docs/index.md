# Eve Genie

A tool for making Eve schema generation easier.

**Use case**: You need to stand up an api quickly. You know what your data looks like in JSON but don't yet know the syntax for Eve/Cerberus.

## Requirements

    sudo pip install -r requirements.txt

## Use

### Cli

    python geneve.py your_json_file

### In code

```python
from evegenie import EveGenie
eg = EveGenie(filename='test.json')
# Or
with open('test.json', 'r') as ifile:
    data = ifile.read()
eg = EveGenie(data=data)
eg.write_file('mytest.settings.py')

```

    cat mytest.settings.py

    user = {
        'schema': {
            'name': {'type': 'string'},
            'title': {'type': 'string'},
            'age': {'type': 'integer'},
            'alive': {'type': 'boolean'},
            'inventory': {'type': 'list'},
            'address': {
                'type': 'dict',
                'schema': {
                    'city': {'type': 'string'},
                    'state': {'type': 'string'},
                    'address': {'type': 'string'},
                }
            }
        }
    }

    artifact = {
        'schema': {
            'color': {'type': 'string'},
            'cost': {'type': 'float'},
            'stats': {
                'type': 'dict',
                'schema': {
                    'length': {'type': 'float'},
                    'weight': {'type': 'float'},
                    'power': {'type': 'integer'},
                }
            }
            'name': {'type': 'string'},
        }
    }

## Special evegenie strings

Certain strings passed in via the source json will be converted to eve schema types with sane defaults.

- `"fieldname": "objectid:sample-entity"` will add data_relation to sample-entity to the schema
- `"fieldname": "0-100"` will create an integer with a min of 0 and a max of 100
- `"fieldname": "0.0-1.0"` will create a float with a min of 0 and a max of 1

## Test

    py.test egtest.py
