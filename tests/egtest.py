#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for geneve tool.
"""

import json
import os
import sys
import pytest
from collections import deque, OrderedDict
from eve.io.mongo import Validator

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from evegenie import EveGenie


test_data = OrderedDict([
    ('user', OrderedDict([
        ('name', 'Turtle Man'),
        ('age', 71),
        ('experience', None),
        ('alive', True),
        ('title', 'Champion of Sea Dwellers'),
        ('inventory', ['map', 'apple', 'sword', 'potion']),
        ('primary_artifact', 'objectid:artifact'),
        ('secondary_artifacts', ['objectid: artifact', 'objectid:artifact']),
        ('address', OrderedDict([
            ('address', '123 Pacific Ocean'),
            ('city', 'Neptunville'),
            ('state', 'wet'),
        ])),
        ('attack_bonus', '1-10'),
        ('difficulty', '0.0-1.0'),
        ('attributes', OrderedDict([('allow_unknown', True)])),
    ])),
    ('artifact', OrderedDict([
        ('name', 'Sword of Speed'),
        ('cost', 501.01),
        ('color', 'red'),
        ('stats', OrderedDict([
            ('weight', 200.01),
            ('length', 3.01),
            ('powers', OrderedDict([
                ('strike', 1),
                ('deflect', 1),
                ('speed', 3),
                ('extra_powers', OrderedDict([('allow_unknown', True)])),
            ])),
        ]))
    ])),
    ('power-up', OrderedDict([
        ('name', 'Star'),
    ]))
])

if not os.path.isfile('test.json'):
    with open('test.json', 'w') as ofile:
        ofile.write(json.dumps(test_data, indent=4, separators=(',',' : ')))

test_data_answer = OrderedDict([
    ('user', OrderedDict([
        ('schema', OrderedDict([
            ('name', OrderedDict([
                ('type', 'string'),
            ])),
            ('age', OrderedDict([
                ('type', 'integer'),
            ])),
            ('experience', OrderedDict([
                ('nullable', True),
            ])),
            ('alive', OrderedDict([
                ('type', 'boolean'),
            ])),
            ('title', OrderedDict([
                ('type', 'string'),
            ])),
            ('inventory', OrderedDict([
                ('type', 'list'),
                ('schema', OrderedDict([
                    ('type', 'string'),
                ])),
            ])),
            ('primary_artifact', OrderedDict([
                ('type', 'objectid'),
                ('data_relation', OrderedDict([
                    ('resource', 'artifact'),
                    ('field', '_id'),
                    ('embeddable', True),
                ])),
            ])),
            ('secondary_artifacts', OrderedDict([
                ('type', 'list'),
                ('schema', OrderedDict([
                    ('type', 'objectid'),
                    ('data_relation', OrderedDict([
                        ('resource', 'artifact'),
                        ('field', '_id'),
                        ('embeddable', True),
                    ])),
                ])),
            ])),
            ('address', OrderedDict([
                ('type', 'dict'),
                ('schema', OrderedDict([
                    ('address', OrderedDict([('type', 'string')])),
                    ('city', OrderedDict([('type', 'string')])),
                    ('state', OrderedDict([('type', 'string')])),
                ])),
            ])),
            ('attack_bonus', OrderedDict([
                ('type', 'integer'),
                ('min', 1),
                ('max', 10),
            ])),
            ('difficulty', OrderedDict([
                ('type', 'float'),
                ('min', 0.0),
                ('max', 1.0),
            ])),
            ('attributes', OrderedDict([
                ('allow_unknown', True),
            ]))
        ])),
    ])),
    ('artifact', OrderedDict([
        ('schema', OrderedDict([
            ('name', OrderedDict([('type', 'string')])),
            ('cost', OrderedDict([('type', 'float')])),
            ('color', OrderedDict([('type', 'string')])),
            ('stats', OrderedDict([
                ('type', 'dict'),
                ('schema', OrderedDict([
                    ('weight', OrderedDict([('type', 'float')])),
                    ('length', OrderedDict([('type', 'float')])),
                    ('powers', OrderedDict([
                        ('type', 'dict'),
                        ('schema', OrderedDict([
                            ('strike', OrderedDict([('type', 'integer')])),
                            ('deflect', OrderedDict([('type', 'integer')])),
                            ('speed', OrderedDict([('type', 'integer')])),
                            ('extra_powers', OrderedDict([('allow_unknown', True)]))
                        ]))
                    ])),
                ]))
            ]))
        ]))
    ])),
    ('power-up', OrderedDict([
        ('schema', OrderedDict([
            ('name', OrderedDict([('type', 'string')])),
        ]))
    ]))
])

simple_test_data = OrderedDict([
    ('user', OrderedDict([
        ('name', 'Turtle Man'),
        ('age', 71),
        ('alive', True),
        ('title', 'Champion of Sea Dwellers'),
    ])),
])

format_endpoint_test = """{
    'schema': {
        'name': {
            'type': 'string'
        },
        'age': {
            'type': 'integer'
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
    assert(OrderedDict(eg) == test_data_answer)


def test_input_dict():
    """
    Make sure data loaded as a dict is parsed as expected.

    :return:
    """
    eg = EveGenie(data=test_data)
    assert(OrderedDict(eg) == test_data_answer)


def test_input_file():
    """
    Make sure data loaded from file is parsed as expected.

    :return:
    """
    eg = EveGenie(filename=parent_dir + '/tests/test.json')
    assert(OrderedDict(eg) == test_data_answer)


def test_input_both_inputs():
    """
    Make sure when both data types are passed the data is still parsed as expected.

    :return:
    """
    eg = EveGenie(data=test_data, filename='test.json')
    assert(OrderedDict(eg) == test_data_answer)


def test_simple_endpoint_validation():
    """
    Test that the endpoint schema generated will validate when used in Eve.

    :return:
    """
    eg = EveGenie(data=simple_test_data)
    data = OrderedDict(eg)
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
    controlfile = parent_dir + '/tests/test.output.py'
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


def test_get_type_ordereddict():
    """
    Test that a OrderedDict maps to an eve 'dict'

    :return:
    """
    source = OrderedDict([('a','b')])
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
