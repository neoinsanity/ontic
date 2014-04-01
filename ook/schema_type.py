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
        CoreType.__init__(self, *args, **kwargs)
        for key, value in self.iteritems():
            if not isinstance(value, SchemaProperty):
                self[key] = SchemaProperty(value)


def perfect_schema(candidate_schema):
    if candidate_schema is None:
        raise ValueError('"candidate_schema" must be provided.')
    if not isinstance(candidate_schema, SchemaType):
        raise ValueError('"candidate_schema" must be of SchemaType.')

    for property_schema in candidate_schema.values():
        meta_type.perfect_schema_property(property_schema)


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
        meta_type.validate_schema_property(candidate_property_schema)

    return value_errors
