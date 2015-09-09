#!/usr/bin/env python
"""
Tests for geneve tool.
"""

import json
import os.path
import pytest
from eve.io.mongo import Validator
from evegenie import EveGenie


test_data = {
    'user': {
        'name': 'Turtle Man',
        'age': 71,
        'alive': True,
        'title': 'Champion of Sea Dwellers',
        'inventory': ['map', 'apple', 'sword', 'potion'],
        'primary_artifact': 'objectid:artifact',
        'secondary_artifacts': ['objectid: artifact', 'objectid:artifact'],
        'address': {
            'address': '123 Pacific Ocean',
            'city': 'Neptunville',
            'state': 'wet',
        },
        'attack_bonus': '1-10',
        'difficulty': '0.0-1.0',
    },
    'artifact': {
        'name': 'Sword of Speed',
        'cost': 501.01,
        'color': 'red',
        'stats': {
            'weight': 200.01,
            'length': 3.01,
            'powers': {
                'strike': 1,
                'deflect': 1,
                'speed': 3,
            },
        }
    }
}

if not os.path.isfile('test.json'):
    with open('test.json', 'w') as ofile:
        ofile.write(json.dumps(test_data, indent=4, separators=(',',' : ')))

test_data_answer = {
    'user': {
        'schema': {
            'name': {
                'type': 'string',
            },
            'age': {
                'type': 'integer',
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
                    'embeddable': True,
                },
            },
            'secondary_artifacts': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'artifact',
                        'field': '_id',
                        'embeddable': True,
                    },
                },
            },
            'address': {
                'type': 'dict',
                'schema': {
                    'address': {'type': 'string'},
                    'city': {'type': 'string'},
                    'state': {'type': 'string'}
                },
            },
            'attack_bonus': {
                'max': 10,
                'min': 1,
                'type': 'integer'
            },
            'difficulty': {
                'max': 1.0,
                'min': 0.0,
                'type': 'float'
            }
        }
    },
    'artifact': {
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
                    'weight': {'type': 'float'},
                    'length': {'type': 'float'},
                    'powers': {
                        'type': 'dict',
                        'schema': {
                            'strike': {'type': 'integer'},
                            'deflect': {'type': 'integer'},
                            'speed': {'type': 'integer'},
                        }
                    },
                }
            }
        }
    }
}

simple_test_data = {
    'user': {
        'name': 'Turtle Man',
        'age': 71,
        'alive': True,
        'title': 'Champion of Sea Dwellers',
    },
}

format_endpoint_test = """{
    'schema': {
        'age': {
            'type': 'integer'
        },
        'name': {
            'type': 'string'
        },
        'alive': {
            'type': 'boolean'
        },
        'title': {
            'type': 'string'
        }
    }
}"""

test_data_answer_string = json.dumps(test_data_answer)


def test_input_string():
    """
    Make sure data loaded from string is parsed as expected.

    :return:
    """
    eg = EveGenie(data=json.dumps(test_data))
    assert(dict(eg) == test_data_answer)


def test_input_dict():
    """
    Make sure data loaded as a dict is parsed as expected.

    :return:
    """
    eg = EveGenie(data=test_data)
    assert(dict(eg) == test_data_answer)


def test_input_file():
    """
    Make sure data loaded from file is parsed as expected.

    :return:
    """
    eg = EveGenie(filename='test.json')
    assert(dict(eg) == test_data_answer)


def test_input_both_inputs():
    """
    Make sure when both data types are passed the data is still parsed as expected.

    :return:
    """
    eg = EveGenie(data=test_data, filename='test.json')
    assert(dict(eg) == test_data_answer)


def test_simple_endpoint_validation():
    """
    Test that the endpoint schema generated will validate when used in Eve.

    :return:
    """
    eg = EveGenie(data=simple_test_data)
    data = dict(eg)
    for endpoint in data:
        v = Validator(data[endpoint]['schema'])
        assert(v.validate(simple_test_data[endpoint]))


def test_endpoint_format():
    """
    Test whether the formatted output for an endpoint is as expected

    :return:
    """
    eg = EveGenie(data=simple_test_data)
    endpoint = eg['user']
    assert(eg.format_endpoint(endpoint) == format_endpoint_test)


if __name__ == '__main__':
    pytest.main('egtest.py')