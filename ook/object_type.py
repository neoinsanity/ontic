"""The fundamental *Ook* base data types for creation of derived child classes.

The **object_type** provides the methods to create and validate **Ook**
types and objects.

.. image:: images/object_type.jpg

Usage
-----

There are two basic operations provided by **object_type**; schema
definition and object
handling. Schema definition entails type creation and validation.

Schema Tools
-------------

To validate a schema definition, utilize the :meth:`~ook.object_type
.validate_schema` method.

Schema are composed of :class:`~ook.object_type.PropertySchema` objects. If
there is a need,
individual **PropertySchema** objects can be validated individually with the
:meth:`~ook.object_type.validate_property` method.

To create a python type for a given :class:`~ook.object_type.SchemaType`
utilize the
:meth:`~ook.object_type.create_ook_type` method. **Ook** object instances
created by a generated
type are child classes of the :class:`~ook.object_types` class.

Object Tools
-------------

**Ook** objects created by either subclassing :class:`ObjectType` or via
:meth:`~create_ook_type`, will need to be validated. Utilize the
**Ook** object :meth:`~ook.object_type.validate_object` method for validation.

If the need should arise for validation of an **Ook** object by value,
utilize the
:meth:`~ook.object_type.validate_value` method.

Usage
------

The **object_type** module allows for the construction of **Ook** data types. A
complete configured data type definition would be constructed as::

    class MyType(ObjectType):
        OOK_SCHEMA = SchemaType({
            'some_property': PropertyType({
                'type': 'int',
                'required': True,
            }),
            'other_property': PropertyType({
                'type': 'str',
                'required': False,
                'enum': {'Enum1', 'Enum2', 'Enum3'}
            }),
        })

    my_object = MyType()
    my_object.some_property = 7
    # or
    my_object['some_property'] = 7

"""

from meta_type import MetaType, PropertySchema
from schema_type import SchemaType


class ObjectType(MetaType):
    """ObjectType provides the **Ook** schema interface.

    The **ObjectType** provides the schema management functionality to a derived
    **Ook** type instance.
    """


def create_ook_type(name, schema):
    """Create an **Ook** type to generate objects with a given schema.

    :param name: The name to apply to the created class, with
        object_type.ObjectType as parent.
    :type name: str
    :param schema: A representation of the schema in dictionary format.
    :type schema: dict
    :return: A class whose base is object_type.ObjectType.
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

    ook_type = type(name, (ObjectType, ), dict())

    if not isinstance(schema, SchemaType):
        schema = SchemaType(schema)

    ook_type.OOK_SCHEMA = schema

    return ook_type


def validate_object(the_object):
    """Method that will validate if an object meets the schema requirements.

    :param the_object: An object instance whose type is a child class of
        :class:`~ook.object_type.ObjectType`
    :type the_object: ook.object_type.ObjectType
    :except ValueError:
        * *the_object* is not a :class:`~ook.object_type.ObjectType`.

        * A property of *the_object* does not meet schema requirements.

    """
    if not isinstance(the_object, ObjectType):
        raise ValueError(
            'Validation can only support validation of objects derived from '
            'ook.ObjectType.')

    value_errors = []

    for property_name, property_schema in the_object.get_schema().iteritems():
        value = the_object.get(property_name, None)

        PropertySchema.validate_value(
            property_name, property_schema, value, value_errors)

    if value_errors:
        raise ValueError(str.join(' \n', value_errors))


def validate_value(property_name, ook_object):
    """Validate a value against a given **PropertySchema**

    :param property_name: The value to be validated against the given
        **PropertySchema**.
    :type property_name: str
    :param ook_object: Ook defined object to be validated.
    :type ook_object: object_type.ObjectType
    :except ValueError:

        - Responds with a value error if the validation is not successful.

        - "property_schema" is not provided or not a dict, **ObjectType**,
            or **PropertySchema**
    """
    if property_name is None:
        raise ValueError(
            '"property_name" is required, cannot be None.')
    if not isinstance(property_name, basestring) or len(property_name) < 1:
        raise ValueError('"property_name" is not a valid string.')
    if ook_object is None:
        raise ValueError(
            '"ook_object" is required, cannot be None.')
    if not isinstance(ook_object, ObjectType):
        raise ValueError(
            '"ook_object" must be ObjectType or child type of ObjectType.')

    value_errors = []

    property_schema = ook_object.get_schema().get(property_name)
    if property_schema is None:
        raise ValueError(
            '"property_name" is not a recognized property.')

    value = ook_object.get(property_name, None)

    PropertySchema.validate_value(
        property_name, property_schema, value, value_errors)

    if value_errors:
        raise ValueError(str.join(' \n', value_errors))
