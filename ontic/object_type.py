"""The fundamental *Ook* base data types for creation of derived child classes.

.. image:: images/object_type.jpg

.. contents::

======
Usage
======

Create Object Types
--------------------

The *object_type* module provides the ::class::`ObjectType` and a set of
functions to handle the creation and validation of *ObjectType* instances.

Construction of **Ook** data types as a class definition::

    >>> class MyType(ObjectType):
    ...     OOK_SCHEMA = SchemaType({
    ...         'some_property': {
    ...             'type': 'int',
    ...             'required': True,
    ...         },
    ...         'other_property': {
    ...             'type': 'str',
    ...             'required': False,
    ...             'enum': {'Enum1', 'Enum2', 'Enum3'}
    ...         },
    ...     })
    >>> my_object = MyType()
    >>> my_object.some_property = 7
    >>> # or
    >>> my_object['some_property'] = 7
    >>> validate_object(my_object)

Dynamic Object Type Definition
-------------------------------

It is also possible to create :class:`ObjectType` derived types dynamically
with the use of the :meth:`create_ook_type` function.

    >>> some_type = create_ook_type('SomeType', {'prop':{'type':'int'}})
    >>> my_object = some_type(prop=3)
    >>> my_object
    {'prop': 3}
    >>> my_object.prop
    3

"""
import meta_type
from meta_type import MetaType, PropertySchema
from schema_type import SchemaType
from validation_exception import ValidationException


class ObjectType(MetaType):
    """ObjectType provides the **Ook** schema interface.

    The **ObjectType** provides the schema management functionality to a derived
    **Ook** type instance.
    """


def create_ook_type(name, schema):
    """Create an **Ook** type to generate objects with a given schema.

    *create_ook_type* function creates an :class:`ObjectType` with a given
    name and schema definition. The schema definition can be a dict instance
    that is a valid  schema definition or a :class:`ontic.schema_type.SchemaType`.
    This makes the following forms valid::

        MyType = create_ook_type('MyType', {'prop':{'type':'int'}})

        schema_instance = SchemaType(prop={'type':'int'})
        MyType = create_ook_type('MyType', schema_instance)

    :param name: The name to apply to the created class, with
        :class:`ObjectType` as parent.
    :type name: str
    :param schema: A representation of the schema in dictionary format.
    :type schema: dict, :class:`ontic.schema_type.SchemaType`
    :return: A class whose base is :class:`ObjectType`.
    :rtype: ClassType
    :raises ValueError: String name required. Dict or
        :class:`ontic.schema_type.SchemaType` schema required.
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


def perfect_object(the_object):
    """Function to ensure complete attribute settings for a given object.

    Perfecting an object instance will strip out any properties not defined in
    the corresponding object type. If there are any missing properties in the
    object, those properties will be added and set to the default value or
    None, if no default has been set.

    :param the_object: Ab object instance that is to be perfected.
    :type the_object: :class:`ook.object_type.ObjectType`
    :rtype: None
    """
    if the_object is None:
        raise ValueError('"the_object" must be provided.')
    if not isinstance(the_object, ObjectType):
        raise ValueError('"the_object" must be ObjectType type.')

    schema = the_object.get_schema()

    extra_properties = set(the_object.keys()) - set(schema.keys())
    for property_name in extra_properties:
        del the_object[property_name]

    for property_name, property_schema in schema.iteritems():
        if property_name not in the_object:
            the_object[property_name] = property_schema.default
            continue
        if not the_object[property_name]:
            the_object[property_name] = property_schema.default


def validate_object(the_object, raise_validation_exception=True):
    """Function that will validate if an object meets the schema requirements.

    :param the_object: An object instant to be validity tested.
    :type the_object: :class:`ObjectType`
    :param raise_validation_exception: If True, then *validate_object* will
        throw a *ValueException* upon validation failure. If False, then a
        list of validation errors is returned. Defaults to True.
    :type raise_validation_exception: bool
    :return: If no validation errors are found, then *None* is
        returned. If validation fails, then a list of the errors is returned
        if the *raise_validation_exception* is set to True.
    :rtype: list<str>, None
    :raises ValueError: if *the_object* is not a
        :class:`~ontic.object_type.ObjectType`.
    :raises:
        * A property of *the_object* does not meet schema requirements.
    """
    if not isinstance(the_object, ObjectType):
        raise ValueError(
            'Validation can only support validation of objects derived from '
            'ontic.object_type.ObjectType.')

    value_errors = []

    for property_name, property_schema in the_object.get_schema().iteritems():
        value = the_object.get(property_name, None)

        errors = validate_value(
            property_name,
            the_object,
            raise_validation_exception=False)
        if errors:
            value_errors.extend(errors)

    if value_errors:
        if raise_validation_exception:
            raise ValidationException(value_errors)
        else:
            return value_errors
    else:
        return None


def validate_value(property_name, ook_object, raise_validation_exception=True):
    """Validate a specific value of a given :class:`ObjectType` instance.

    :param property_name: The value to be validated against the given
        **PropertySchema**.
    :type property_name: str
    :param ook_object: Ook defined object to be validated.
    :type ook_object: object_type.ObjectType
    :param raise_validation_exception: If True, then *validate_object* will
        throw a *ValueException* upon validation failure. If False, then a
        list of validation errors is returned. Defaults to True.
    :type raise_validation_exception: bool
    :return: If no validation errors are found, then *None* is
        returned. If validation fails, then a list of the errors is returned
        if the *raise_validation_exception* is set to True.
    :rtype: list<str>, None
    :raises ValueError: If *property_name* is not provided or is not a valid
        string.
    :raises ValueError: If *ook_object* is None, or not instance of
        *ObjectType*.
    :raises ValidationException: If the validation is not successful. The
        *ValidationException* will not be raised if
        *raise_validation_exception* is
        set to False.
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

    value_errors.extend(
        meta_type.validate_value(property_name, property_schema, value))

    if value_errors:
        if raise_validation_exception:
            raise ValidationException(value_errors)
        else:
            return value_errors
    else:
        return None
