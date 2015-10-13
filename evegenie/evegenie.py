"""
EveGenie class for building Eve settings and schemas.
"""
import json
import os.path
import re
from types import NoneType
from collections import OrderedDict

from jinja2 import Environment, PackageLoader


class EveGenie(object):

    template_env = Environment(loader=PackageLoader('evegenie', 'templates'))
    # 'objectid:sample-endpoint' or 'objectid: sample-endpoint'
    objectidregex = re.compile('^objectid:\s*?(.+)$', flags=re.M)
    # 'int-int' or 'int - int'. eg: '1-10'
    intrangeregex = re.compile('^(\d+)\s*?-\s*?(\d+)$', flags=re.M)
    # 'float-float' or 'float - float'. eg: 0.0-1.0
    floatrangeregex = re.compile('^([0-9.]+)\s*?-\s*?([0-9.]+)$', flags=re.M)


    def __init__(self, data=None, filename=None):
        """
        Initialize EveGenie object. Parses input and sets each endpoint from
        input as an attribute on the EveGenie object.

        :param data: string or dict of the json representation of our schema
        :param filename: file containing json representation of our schema
        :return:
        """
        self.endpoints = OrderedDict()

        if filename and not data:
            if os.path.isfile(filename):
                with open(filename, 'r') as ifile:
                    data = ifile.read().strip()

        if not isinstance(data, (basestring, dict, OrderedDict)):
            raise TypeError('Input is not a string: {}'.format(data))
            sys.exit(1)

        if isinstance(data, basestring):
            data = json.loads(data, object_pairs_hook=OrderedDict)

        self.endpoints = OrderedDict([(k, OrderedDict([('schema', self.parse_endpoint(v))])) for k, v in data.iteritems()])

    def parse_endpoint(self, endpoint_source):
        """
        Takes the values of an endpoint from its raw json representation and
        converts it to the eve schema equivalent.

        :param endpoint_source: dict of fields in an endpoint
        :return: dict representing eve schema for the endpoint
        """
        return OrderedDict([(k, self.parse_item(v)) for k, v in endpoint_source.iteritems()])

    def parse_item(self, endpoint_item):
        """
        Recursivily takes the values of an endpoint's field from its raw
        json and convets it to the eve schema equivalent of that field.

        :param endpoint_item: dict of field within an endpoint
        :return: dict representing eve schema for field
        """
        item = OrderedDict([('type', self.get_type(endpoint_item))])
        if item['type'] == 'dict':
            # recursively parse each item in a dict and add to item schema
            item['schema'] = OrderedDict()
            for k, i in endpoint_item.iteritems():
                item['schema'][k] = self.parse_item(i)

                # if allow_unknown, remove the type and set allow_unknown.
                if k == 'allow_unknown' and isinstance(i, bool):
                    del item['schema']
                    del item['type']
                    item[k] = i
        elif item['type'] == 'list':
            # recursively parse each item in a list and add to item schema
            item['schema'] = OrderedDict()
            for i in endpoint_item:
                item['schema'] = self.parse_item(i)
        elif item['type'] == 'objectid':
            # add extra data_relation for objectid types
            match = self.objectidregex.match(endpoint_item).group(1)
            if match:
                item['data_relation'] = OrderedDict([
                    ('resource', match),
                    ('field', '_id'),
                    ('embeddable', True),
                ])
        elif item['type'] == 'integer':
            # if string, it's really an integer range
            if isinstance(endpoint_item, basestring):
                match = self.intrangeregex.match(endpoint_item).group(1, 2)
                if match:
                    item['min'] = int(match[0])
                    item['max'] = int(match[1])
        elif item['type'] == 'float':
            # if string, it's really a float range
            if isinstance(endpoint_item, basestring):
                match = self.floatrangeregex.match(endpoint_item).group(1, 2)
                if match:
                    item['min'] = float(match[0])
                    item['max'] = float(match[1])
        elif item['type'] == 'null':
            # if null, don't assume any type, just set nullable to true.
            item['nullable'] = True
            del item['type']

        return item

    def get_type(self, source):
        """
        Map python value types to Eve schema value types.

        :param source: value from source json field
        :return: eve schema type representing source type
        """
        type_mapper = {
            unicode: 'string',
            str: 'string',
            bool: 'boolean',
            int: 'integer',
            float: 'float',
            dict: 'dict',
            list: 'list',
            OrderedDict: 'dict',
            NoneType: 'null',
        }
        source_type = type(source)

        if source_type in type_mapper:
            eve_type = type_mapper[source_type]
        else:
            raise TypeError('Value types must be in [{0}]'.format(', '.join(type_mapper.values())))

        # Evegenie special strings
        if eve_type == 'string':
            if self.objectidregex.match(source):
                eve_type = 'objectid'
            elif self.intrangeregex.match(source):
                eve_type = 'integer'
            elif self.floatrangeregex.match(source):
                eve_type = 'float'

        return eve_type

    def format_endpoint(self, endpoint_schema):
        """
        Render endpoint schema for readability.  This adds indentation and line breaks.

        :param endpoint_schema: dict of eve schema
        :return string of eve schema ready for output
        """

        # separators prevents trailing whitespace, sort_keys false keeps order of ordereddict
        endpoint = json.dumps(endpoint_schema, indent=4, separators=(',', ': '), sort_keys=False)
        updates = [
            ('"', '\''), # replace doubles with singles
            ('true', 'True'), # convert json booleans to python ones
            ('false', 'False')
        ]
        for needle, sub in updates:
            endpoint = endpoint.replace(needle, sub)

        return endpoint

    def write_file(self, filename):
        """
        Pass schema object to template engine to be rendered for use.

        :param filename: output filename
        :return:
        """
        template = self.template_env.get_template('settings.py.j2')

        settings = template.render(
            endpoints=OrderedDict([(endpoint, self.format_endpoint(schema)) for endpoint, schema in self.endpoints.iteritems()])
        )
        with open(filename, 'w') as ofile:
            ofile.write(settings + "\n")

    def __iter__(self):
       for k, v in self.endpoints.iteritems():
          yield k, v

    def __repr__(self):
        return json.dumps(self.endpoints)

    def __str__(self):
        return json.dumps(self.endpoints, indent=4, separators=(',', ': '))

    def __len__(self):
        return len(self.endpoints)

    def __getitem__(self, k):
        return self.endpoints[k]

    def __sizeof__(self):
        return len(self.endpoints)
