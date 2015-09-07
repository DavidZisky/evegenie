"""
EveGenie class for building Eve settings and schemas.
"""
import json
import os.path
import re

from jinja2 import Environment, PackageLoader


class EveGenie(object):

    template_env = Environment(loader=PackageLoader('evegenie', 'templates'))
    objectidregex = re.compile('^objectid:\s*?(.+)$', flags=re.M)
    intrangeregex = re.compile('^(\d+)-(\d+)$', flags=re.M)
    floatrangeregex = re.compile('^([0-9.]+)-([0-9.]+)$', flags=re.M)


    def __init__(self, data=None, filename=None):
        """
        Initialize EveGenie object. Parses input and sets each endpoint from
        input as an attribute on the EveGenie object.

        :param data: string or dict of the json representation of our schema
        :param filename: file containing json representation of our schema
        :return:
        """

        if filename and not data:
            if os.path.isfile(filename):
                with open(filename, 'r') as ifile:
                    data = ifile.read().strip()

        if not isinstance(data, (basestring, dict)):
            raise TypeError('Input is not a string: {}'.format(data))
            sys.exit(1)

        if isinstance(data, basestring):
            data = json.loads(data)

        source = data
        for endpoint in source:
            setattr(self, endpoint, self.parse_endpoint(source[endpoint]))


    def parse_endpoint(self, endpoint_source):
        """
        Takes the values of an endpoint from its raw json representation and
        converts it to the eve schema equivalent.

        :param endpoint_source: dict of fields in an endpoint
        :return: dict representing eve schema for the endpoint
        """
        schema = {}
        for key, value in endpoint_source.iteritems():
            schema[key] = self.parse_item(value)

        return schema


    def parse_item(self, endpoint_item):
        """
        Recursivily takes the values of an endpoint's field from its raw
        json and convets it to the eve schema equivalent of that field.

        :param endpoint_item: dict of field within an endpoint
        :return: dict representing eve schema for field
        """
        item = {'type': self.get_type(endpoint_item)}
        if item['type'] == 'dict':
            # recursively parse each item in a dict and add to item schema
            item['schema'] = {}
            for k, i in endpoint_item.iteritems():
                item['schema'][k] = self.parse_item(i)
        elif item['type'] == 'list':
            # recursively parse each item in a list and add to item schema
            item['schema'] = {}
            for i in endpoint_item:
                item['schema'] = self.parse_item(i)
        elif item['type'] == 'objectid':
            # add extra data_relation for objectid types
            match = self.objectidregex.match(endpoint_item).group(1)
            if match:
                item['data_relation'] = {
                    'resource': match,
                    'field': '_id',
                    'embeddable': True,
                }
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
        }
        source_type = type(source)

        if source_type in type_mapper:
            eve_type = type_mapper[source_type]
        else:
            raise TypeError('Value types must be unicode, str, bool, int, float, dict, or list')

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
        :param endpoint_schema: dict of eve schema
        :return string of eve schema ready for output
        """
        # separators prevents trailing whitespace
        endpoint = json.dumps(endpoint_schema, indent=4, separators=(',',' : '))
        endpoint.replace('"', '\'') \
                .replace('true', 'True') \
                .replace('false', 'False')

        return endpoint


    def write_file(self, filename):
        """
        Pass schema object to template engine to be rendered for use.

        :param filename: output filename
        :return:
        """
        template = self.template_env.get_template('settings.py.j2')

        settings = template.render(
            endpoints = {
                endpoint: self.format_endpoint(endpoint_schema) \
                    for endpoint, endpoint_schema in self.__dict__.iteritems()
            }
        )
        with open(filename, 'w') as ofile:
            ofile.write(settings)


    def __str__(self):
        return json.dumps(self.__dict__)
