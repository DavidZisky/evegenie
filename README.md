# Eve Genie

A tool for making Eve schema generation easier.

## Requirements

    sudo pip install -r requirements.txt

## Use

### Cli

    python geneve.py your_json_file

### In code

```py
from evegenie import EveGenie
eg = EveGenie(filename='test.json')
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

## Test

    py.test egtest.py