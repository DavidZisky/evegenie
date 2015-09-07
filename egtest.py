#!/usr/bin/env python
"""
Tests for geneve tool.
"""

import json
from evegenie import EveGenie


test_data = {
    'user': {
        'name': 'Turtle Man',
        'age': 71,
        'title': 'Champion of Sea Dwellers',
        'inventory': ['map', 'apple', 'sword', 'potion'],
        'address': {
            'address': '123 Pacific Ocean',
            'city': 'Neptunville',
            'state': 'wet',
        }
    }
}

test_data_answer = {
    'user': {
        'name': {
            'type': 'string',
        },
        'age': {
            'type': 'integer',
        },
        'title': {
            'type': 'string'
        },
        'inventory': {
            'type': 'list'
        },
        'address': {
            'type': 'dict',
            'schema': {
                'address': {'type': 'string'},
                'city': {'type': 'string'},
                'state': {'type': 'string'}
            },
        }
    }
}

test_data_answer_string = json.dumps(test_data_answer)


def test_input_string():
    """
    Make sure data loaded from string is parsed as expected.

    :return:
    """
    eg = EveGenie(data=json.dumps(test_data))
    assert(json.loads(str(eg)) == test_data_answer)


def test_input_dict():
    """
    Make sure data loaded as a dict is parsed as expected.

    :return:
    """
    eg = EveGenie(data=test_data)
    assert(json.loads(str(eg)) == test_data_answer)


def test_input_file():
    """
    Make sure data loaded from file is parsed as expected.

    :return:
    """
    eg = EveGenie(filename='test.json')
    assert(json.loads(str(eg)) == test_data_answer)


def test_input_both_inputs():
    """
    Make sure when both data types are passed the data is still parsed as expected.
    
    :return:
    """
    eg = EveGenie(data=test_data, filename='test.json')
    assert(json.loads(str(eg)) == test_data_answer)
