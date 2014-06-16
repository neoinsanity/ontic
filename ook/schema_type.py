"""The classes utilized to construct schemas for object definitions.

Usage
------

Classes
--------

"""
from ook import meta_type
from ook.meta_type import CoreType, SchemaProperty


class SchemaType(CoreType):
    """The type definition for a schema object.

    The **SchemaType** contains a dictionary of property field names and
    the corresponding **SchemaProperty** definition.

    Example SchemaType representation::

        SchemaType({
          'some_property': SchemaProperty({
                'type': 'str',
                'required': True
            })
        })
    """

    def __init__(self, *args, **kwargs):
        """

        dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)

        :param seq:
        :param kwargs:
        :return:
        """
        super(SchemaType, self).__init__(*args, **kwargs)
        for key, value in self.iteritems():
            if not isinstance(value, SchemaProperty):
                self[key] = SchemaProperty(value)

    @staticmethod
    def perfect_schema(candidate_schema):
        """

        :param candidate_schema:
        :type candidate_schema:
        :return:
        :rtype:
        """
        if candidate_schema is None:
            raise ValueError('"candidate_schema" must be provided.')
        if not isinstance(candidate_schema, SchemaType):
            raise ValueError('"candidate_schema" must be of SchemaType.')

        for property_schema in candidate_schema.values():
            SchemaProperty.perfect_schema_property(property_schema)

    @staticmethod
    def validate_schema(candidate_schema):
        """

        :param candidate_schema:
        :type candidate_schema:
        :return:
        :rtype:
        """
        if candidate_schema is None:
            raise ValueError('"candidate_schema" must be provided.')
        if not isinstance(candidate_schema, SchemaType):
            raise ValueError('"candidate_schema" must be of SchemaType.')

        value_errors = []
        for candidate_property_schema in candidate_schema.values():
            SchemaProperty.validate_schema_property(
                candidate_property_schema, value_errors)

        return value_errors
