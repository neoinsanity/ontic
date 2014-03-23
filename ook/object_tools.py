"""The **object_tools** provides the methods to create and validate **Ook**
types and objects.

Usage
======

There are two basic operations provided by **object_tools**; schema
definition and object
handling. Schema definition entails type creation and validation.

Schema Tools
-------------

To validate a schema definition, utilize the :meth:`~ook.object_tools
.validate_schema` method.

Schema are composed of :class:`~ook.object_type.PropertySchema` objects. If
there is a need,
individual **PropertySchema** objects can be validated individually with the
:meth:`~ook.object_tools.validate_property` method.

To create a python type for a given :class:`~ook.object_type.SchemaType`
utilize the
:meth:`~ook.object_tools.create_ook_type` method. **Ook** object instances
created by a generated
type are child classes of the :class:`~ook.object_types` class.

Object Tools
-------------

**Ook** objects created by either subclassing :class:`~ook.object_type
.BaseType` or via
:meth:`~create_ook_type`, will need to be validated. Utilize the
**Ook** object :meth:`~ook.object_tools.validate_object` method for validation.

If the need should arise for validation of an **Ook** object by value,
utilize the
:meth:`~ook.object_tools.validate_value` method.

"""
import re

from object_type import BaseType
from ook import meta_tools
from schema_type import SchemaProperty, SchemaType


def create_ook_type(name, schema):
    """Create an **Ook** type to generate objects with a given schema.

    :param name: The name to apply to the created class, with object_type
    .BaseType as parent.
    :type name: str
    :param schema: A representation of the schema in dictionary format.
    :type schema: dict
    :return: A class whose base is object_type.BaseType.
    :rtype: ClassType
    :except ValueError: String name required. Dict or SchemaType schema
    required.
    """
    if name is None or name is '':
        raise ValueError('The string "name" argument is required.')
    if schema is None:
        raise ValueError('The schema dictionary is required.')
    if not isinstance(schema, dict):
        raise ValueError('The schema must be a dict or SchemaType.')

    ook_type = type(name, (BaseType, ), dict())

    if not isinstance(schema, SchemaType):
        schema = SchemaType(schema)

    ook_type._OOK_SCHEMA = schema

    return ook_type


def validate_object(the_object):
    """Method that will validate if an object meets the schema requirements.

    :param the_object: An object instance whose type is a child class of
        :class:`~ook.object_type.BaseType`
    :type the_object: ook.object_type.BaseType
    :except ValueError:
        * *the_object* is not a :class:`~ook.object_type.BaseType`.

        * A property of *the_object* does not meet schema requirements.

    """
    if not isinstance(the_object, BaseType) and not isinstance(the_object,
                                                               SchemaProperty):
        raise ValueError(
            'Validation can only support validation of objects derived from '
            'ook.BaseType.')

    value_errors = []

    for property_name, property_schema in the_object.get_schema().iteritems():
        value = the_object.get(property_name, None)

        meta_tools._validate_value(
            property_name, property_schema, value, value_errors)

    if value_errors:
        raise ValueError(str.join(' \n', value_errors))


def validate_schema(property_schema):
    """Determine if a schema definition is a valid :class:`~ook.object_type
    .SchemaType` candidate.

    :param property_schema: The schema definition candidate.
    :type property_schema: dict|schema_type.SchemaType
    :except ValueError:

        * *property_schema* is not a dict, **BaseType**, or *SchemaType*.

        * *property_schema* is not a valid **Ook** schema definition.
    """
    if not isinstance(property_schema, dict):
        raise ValueError(
            '"property_schema" argument must be of type dict, BaseType, '
            'or SchemaType,')

    if not isinstance(property_schema, SchemaProperty):
        SchemaProperty(property_schema)
    else:
        validate_object(property_schema)


def validate_value(value, property_schema):
    """Validate a value against a given **SchemaProperty**

    :param value: The value to be validated against the given
    **SchemaProperty**.
    :type value: object
    :param property_schema: The **SchemaProperty** utilized for validation.
    :type property_schema:  dict, ook.object_tools.BaseType, ook.object_tools
    .SchemaProperty
    :except ValueError:

        - Responds with a value error if the validation is not successful.

        - "property_schema" is not provided or not a dict, **BaseType**,
        or **SchemaProperty**
    """
    if property_schema is None:
        raise ValueError('"property_schema" is not provided.')
    if not isinstance(property_schema, dict):
        raise ValueError(
            '"property_schema" is not of type dict, BaseType, '
            'or SchemaProperty.')

    if not isinstance(property_schema, SchemaProperty):
        property_schema = SchemaProperty(property_schema)

    value_errors = []

    meta_tools._validate_value('value', property_schema, value, value_errors)

    if value_errors:
        raise ValueError(str.join(' \n', value_errors))

