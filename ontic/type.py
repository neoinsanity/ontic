"""The fundamental *Ontic* base data types for creation of derived child
classes.

.. image:: images/ontic_type.jpg

.. contents::

======
Usage
======

Create Ontic Types
--------------------

The *ontic_type* module provides the :class:`OnticType` and a set of
functions to handle the creation and validation of *OnticType* instances.

Construction of **Ontic** data types as a class definition::

    >>> class MyType(OnticType):
    ...     ONTIC_SCHEMA = Schema({
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
    []

Dynamic Ontic Type Definition
-------------------------------

It is also possible to create :class:`OnticType` derived types dynamically
with the use of the :meth:`create_ontic_type` function.

    >>> some_type = create_ontic_type('SomeType', {'prop':{'type':'int'}})
    >>> my_object = some_type(prop=3)
    >>> my_object
    {'prop': 3}
    >>> my_object.prop
    3

"""
from copy import deepcopy
from typing import List, Union

from ontic import meta
from ontic.meta import Meta, COLLECTION_TYPES, TYPE_MAP
from ontic.schema import Schema
from ontic.validation_exception import ValidationException


class OnticType(Meta):
    """OnticType provides the **Ontic** schema interface.

    The **OnticType** provides the schema management functionality to a
    derived **Ontic** type instance.
    """

    def perfect(self) -> None:
        """Function to ensure complete attribute settings for a given object.

        Perfecting an object instance will strip out any properties not
        defined in
        the corresponding object type. If there are any missing properties in
        the
        object, those properties will be added and set to the default value or
        None, if no default has been set.

        For the collection types (dict, list, set), the default values are deep
        copied.

        :rtype: None
        """
        perfect_object(self)

    def validate(self, raise_validation_exception: bool = True) -> List[str]:
        """Validate the given OnticType instance against it's defined schema.

        :param raise_validation_exception: If True, then *validate_object* will
            throw a *ValueException* upon validation failure. If False, then a
            list of validation errors is returned. Defaults to True.
        :type raise_validation_exception: bool
        :return: If no validation errors are found, then *None* is
            returned. If validation fails, then a list of the errors is returned
            if the *raise_validation_exception* is set to True.
        :rtype: list<str>, None
        """
        return validate_object(self, raise_validation_exception)

    def validate_value(self,
                       value_name: str,
                       raise_validation_exception: bool = True) -> List[str]:
        """Validate a target value of a given ontic object.

        :param value_name: The value name to validate.
        :type value_name: str
        :param raise_validation_exception: If True, then *validate_object* will
            throw a *ValueException* upon validation failure. If False, then a
            list of validation errors is returned. Defaults to True.
        :type raise_validation_exception: bool
        :return: If no validation errors are found, then *None* is
            returned. If validation fails, then a list of the errors is returned
            if the *raise_validation_exception* is set to True.
        :rtype: list<str>, None
        """
        return validate_value(value_name, self, raise_validation_exception)


def create_ontic_type(name: str, schema: Union[dict, Schema]) -> type:
    """Create an **Ontic** type to generate objects with a given schema.

    *create_ontic_type* function creates an :class:`OnticType` with a given
    name and schema definition. The schema definition can be a dict instance
    that is a valid  schema definition or a
    :class:`ontic.schema_type.SchemaType`. This makes the following forms
    valid::

        MyType = create_ontic_type('MyType', {'prop':{'type':'int'}})

        schema_instance = SchemaType(prop={'type':'int'})
        MyType = create_ontic_type('MyType', schema_instance)

    :param name: The name to apply to the created class, with
        :class:`OnticType` as parent.
    :type name: str
    :param schema: A representation of the schema in dictionary format.
    :type schema: dict, :class:`ontic.schema_type.SchemaType`
    :return: A class whose base is :class:`OnticType`.
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

    ontic_type = type(name, (OnticType,), dict())

    if not isinstance(schema, Schema):
        schema = Schema(schema)

    ontic_type.ONTIC_SCHEMA = schema

    return ontic_type


def perfect_object(the_object: OnticType) -> None:
    """Function to ensure complete attribute settings for a given object.

    Perfecting an object instance will strip out any properties not defined in
    the corresponding object type. If there are any missing properties in the
    object, those properties will be added and set to the default value or
    None, if no default has been set.

    For the collection types (dict, list, set), the default values are deep
    copied.

    :param the_object: Ab object instance that is to be perfected.
    :type the_object: :class:`ontic.type.OnticType`
    :rtype: None
    """
    if the_object is None:
        raise ValueError('"the_object" must be provided.')
    if not isinstance(the_object, OnticType):
        raise ValueError('"the_object" must be OnticType type.')

    schema = the_object.get_schema()

    extra_properties = set(the_object.keys()) - set(schema.keys())
    for property_name in extra_properties:
        del the_object[property_name]

    for property_name, property_schema in schema.items():
        if property_name not in the_object:
            the_object[property_name] = None
        value = the_object[property_name]

        if value is None and property_schema.default is not None:
            if TYPE_MAP.get(property_schema.type) in COLLECTION_TYPES:
                value = the_object[property_name] = deepcopy(
                    property_schema.default)
            elif issubclass(property_schema.type, OnticType):
                value = the_object[property_name] = deepcopy(
                    property_schema.default)
            else:
                value = the_object[property_name] = property_schema.default

        if value is not None and isinstance(value, OnticType):
            value.perfect()


def validate_object(
        the_object: OnticType,
        raise_validation_exception: bool = True) -> List[str]:
    """Function that will validate if an object meets the schema requirements.

    :param the_object: An object instant to be validity tested.
    :type the_object: :class:`OnticType`
    :param raise_validation_exception: If True, then *validate_object* will
        throw a *ValueException* upon validation failure. If False, then a
        list of validation errors is returned. Defaults to True.
    :type raise_validation_exception: bool
    :return: If no validation errors are found, then *None* is
        returned. If validation fails, then a list of the errors is returned
        if the *raise_validation_exception* is set to True.
    :rtype: list<str>, None
    :raises ValueError: If *the_object* is None or not of type
        :class:`~ontic.ontic_type.OnticType`.
    :raises ValidationException: A property of *the_object* does not meet
        schema requirements.
    """
    if not isinstance(the_object, OnticType):
        raise ValueError(
            'Validation can only support validation of objects derived from '
            'ontic.ontic_type.OnticType.')

    value_errors = []

    for property_name in the_object.get_schema().keys():
        value_errors.extend(validate_value(property_name, the_object, False))

    if value_errors and raise_validation_exception:
        raise ValidationException(value_errors)

    return value_errors


def validate_value(property_name: str,
                   ontic_object: OnticType,
                   raise_validation_exception: bool = True) -> List[str]:
    """Validate a specific value of a given :class:`OnticType` instance.

    :param property_name: The value to be validated against the given
        **PropertyType**.
    :type property_name: str
    :param ontic_object: Ontic defined object to be validated.
    :type ontic_object: type.OnticType
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
    :raises ValueError: If *ontic_object* is None, or not instance of
        *OnticType*.
    :raises ValidationException: If the validation is not successful. The
        *ValidationException* will not be raised if
        *raise_validation_exception* is
        set to False.
    """
    if property_name is None:
        raise ValueError(
            '"property_name" is required, cannot be None.')
    if not isinstance(property_name, str) or len(property_name) < 1:
        raise ValueError('"property_name" is not a valid string.')
    if ontic_object is None:
        raise ValueError(
            '"ontic_object" is required, cannot be None.')
    if not isinstance(ontic_object, OnticType):
        raise ValueError(
            '"ontic_object" must be OnticType or child type of OnticType.')

    value_errors = []

    property_schema = ontic_object.get_schema().get(property_name)
    if property_schema is None:
        raise ValueError(
            '"%s" is not a recognized property.' % property_name)

    value = ontic_object.get(property_name, None)

    value_errors.extend(
        meta.validate_value(property_schema, value))

    # if a value is an OnticType, then have it self validate.
    is_ontic_type = (property_schema.type is not None and
                     issubclass(property_schema.type, OnticType))
    child_errors = None
    if is_ontic_type and value is not None:
        child_errors = value.validate(raise_validation_exception=False)
    if child_errors:
        error_msg = 'The child property %s, has errors:: %s' % (
            property_name, ' || '.join(child_errors))
        value_errors.append(error_msg)

    if value_errors and raise_validation_exception:
        raise ValidationException(value_errors)

    return value_errors
