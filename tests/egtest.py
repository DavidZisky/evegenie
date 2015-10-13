#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for geneve tool.
"""

import json
import os
import sys
import pytest
from collections import deque
from eve.io.mongo import Validator

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from evegenie import EveGenie


test_data = {
    'user': {
        'name': 'Turtle Man',
        'age': 71,
        'experience': None,
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
        'attributes': {'allow_unknown': True},
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
                'extra_powers': {'allow_unknown': True},
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
            'experience': {
                'nullable': True,
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
            },
            'attributes': {
                'allow_unknown': True
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
                            'extra_powers': {'allow_unknown': True}
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

def test_evegenie_no_data():
    """
    Test that attempting to initilaize EveGenie object with no data errors.

    :return:
    """
    with pytest.raises(TypeError):
        eg = EveGenie()


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


def test_output_file():
    """
    Tests writing schema to file and compares the files output to a control.

    :return:
    """
    outfile = parent_dir + '/tests/test_output'
    controlfile = parent_dir + '/tests/.test_out_control'
    eg = EveGenie(data=test_data)

    with open(controlfile, 'r') as ifile:
        control = ifile.read()

    eg.write_file(outfile)
    with open(outfile, 'r') as ifile:
        test_schema = ifile.read()

    os.remove(outfile)
    assert(test_schema == control)


def test_get_type_unicode():
    """
    Test that a unicode string maps to an eve 'string'

    :return:
    """
    source = '☃'
    eg = EveGenie(data=simple_test_data)
    assert(eg.get_type(source) == 'string')


def test_get_type_str():
    """
    Test that a str maps to an eve 'string'

    :return:
    """
    source = 'snowman'
    eg = EveGenie(data=simple_test_data)
    assert(eg.get_type(source) == 'string')


def test_get_type_bool():
    """
    Test that a bool maps to an eve 'boolean'

    :return:
    """
    source = True
    eg = EveGenie(data=simple_test_data)
    assert(eg.get_type(source) == 'boolean')


def test_get_type_int():
    """
    Test that an int maps to an eve 'integer'

    :return:
    """
    source = 42
    eg = EveGenie(data=simple_test_data)
    assert(eg.get_type(source) == 'integer')


def test_get_type_float():
    """
    Test that a float maps to an eve 'float'

    :return:
    """
    source = 4.2
    eg = EveGenie(data=simple_test_data)
    assert(eg.get_type(source) == 'float')


def test_get_type_dict():
    """
    Test that a dict maps to an eve 'dict'

    :return:
    """
    source = {'a':'b'}
    eg = EveGenie(data=simple_test_data)
    assert(eg.get_type(source) == 'dict')


def test_get_type_list():
    """
    Test that a list maps to an eve 'list'

    :return:
    """
    source = [1, 2, 3]
    eg = EveGenie(data=simple_test_data)
    assert(eg.get_type(source) == 'list')


def test_get_type_objectid():
    """
    Test that an objectid string maps to an eve 'objectid'

    :return:
    """
    source = 'objectid:test'
    eg = EveGenie(data=simple_test_data)
    assert(eg.get_type(source) == 'objectid')


def test_get_type_intrange():
    """
    Test that an integer range string maps to an eve 'integer'

    :return:
    """
    source = "1-10"
    eg = EveGenie(data=simple_test_data)
    assert(eg.get_type(source) == 'integer')


def test_get_type_floatrange():
    """
    Test that a float range string maps to an eve 'float'

    :return:
    """
    source = "0.0-1.0"
    eg = EveGenie(data=simple_test_data)
    assert(eg.get_type(source) == 'float')


def test_get_type_null():
    """
    Test that a None maps to an eve 'null'.

    :return:
    """
    source = None
    eg = EveGenie(data=simple_test_data)
    assert(eg.get_type(source) == 'null')


def test_get_type_fail():
    """
    Test that type correctly errors when an invalid type is passed.

    :return:
    """
    source = deque('abc')
    eg = EveGenie(data=simple_test_data)
    with pytest.raises(TypeError):
        eg.get_type(source)


def test_evegenie_len():
    """
    Test that an EveGenie object correctly reports its length.

    :return:
    """
    eg = EveGenie(data=simple_test_data)
    assert(len(eg) == 1)


if __name__ == '__main__':
    pytest.main('{}/tests/egtest.py'.format(parent_dir))
