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
    eg = EveGenie(data=json.dumps(test_data))
    assert(json.loads(str(eg)) == test_data_answer)


def test_input_dict():
    eg = EveGenie(data=test_data)
    assert(json.loads(str(eg)) == test_data_answer)


def test_input_file():
    eg = EveGenie(filename='test.json')
    assert(json.loads(str(eg)) == test_data_answer)


def test_input_both_inputs():
    eg = EveGenie(data=test_data, filename='test.json')
    assert(json.loads(str(eg)) == test_data_answer)
