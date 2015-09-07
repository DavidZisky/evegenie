"""
EveGenie class for building Eve settings and schemas.
"""
import json
import os.path

from jinja2 import Environment, PackageLoader


class EveGenie(object):

    template_env = Environment(loader=PackageLoader('evegenie', 'templates'))

    def __init__(self, data=None, filename=None):
        """
        Initialize EveGenie object. Parses input and sets each endpoint from
        input as an attribute on the EveGenie object.

        :param data: string or dict of the json representation of our schema
        :param filename: file containing json representation of our schema
        :return:
        """
        self.endpoints = {}

        if filename and not data:
            if os.path.isfile(filename):
                with open(filename, 'r') as ifile:
                    data = ifile.read().strip()

        if not isinstance(data, (basestring, dict)):
            raise TypeError('Input is not a string: {}'.format(data))
            sys.exit(1)

        if isinstance(data, basestring):
            data = json.loads(data)

        self.endpoints = {k: self.parse_endpoint(v) for k, v in data.iteritems()}

    def parse_endpoint(self, endpoint_source):
        """
        Takes the values of an endpoint from its raw json representation and
        converts it to the eve schema equivalent.

        :param endpoint_source: dict of fields in an endpoint
        :return: dict representing eve schema for the endpoint
        """

        return {k: self.parse_item(v) for k, v in endpoint_source.iteritems()}

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
            item['data_relation'] = {
                # 9 from 'objectid:', strip to allow for space after colon
                'resource': endpoint_item[9:].strip(),
                'field': '_id',
                'embeddable': True,
            }

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
            if source[:9] == 'objectid:':
                eve_type = 'objectid'

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
            endpoints={
                endpoint: self.format_endpoint(schema) for endpoint, schema in self.endpoints.iteritems()
            }
        )
        with open(filename, 'w') as ofile:
            ofile.write(settings)

    def __str__(self):
        return json.dumps(self.endpoints)
