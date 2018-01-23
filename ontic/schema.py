"""The classes utilized to construct schemas for object definitions.

.. image:: images/ontic_schema.jpg

.. contents::

======
Usage
======

The *schema_type* module contains the class :class:`Schema` and a set of
functions to create and validate schema. *Schema* are used to validate
:class:`ontic.ontic_type.OnticType` derived instances.

Creating Schema
----------------

A *Schema* is defined as a dictionary with the key entry being the name
of the property. The value portion of the dictionary is a
:class:`ontic.meta_type.PropertySchema` instance::

    >>> a_schema = Schema([
    ...     property.OnticProperty(name='property_name', type= 'str')
    ... ])

While the example above give a strict definition of a schema, creation of a
schema can omit the use of the *PropertySchema*, as the *Schema*
instantiation will convert a dict value to a *PropertySchema* object. The
above example can be simplified to be::

    >>> a_schema = Schema([
    ...     {'name': 'property_name', 'type': 'str'}
    ... ])

The *Schema* also supports the dict style of instantiation via parameter
naming::

    >>> a_schema = Schema(property_name={'type': 'str'})

Dynamic Schema
-----------------

In cases where necessary, a *Schema* can be created dynamically::

    >>> a_schema = Schema()
    >>> a_schema.add(property.OnticProperty({'name': 'a', 'type': 'str'}))

To aid in the handling of dynamic models, utilize the :meth:`perfect_schema`
and :meth:`validate_schema`.

    >>> perfect_schema(a_schema)
    >>> errors = validate_schema(a_schema)

"""
import logging
from typing import List, Union

from ontic import core
from ontic import property
from ontic.validation_exception import ValidationException


class Schema(core.Core):
    """The type definition for a schema object.

    The **Schema** contains a dictionary of property field names and
    the corresponding **OnticProperty** definition.

    Example Schema representation::

        Schema({
          'some_property': Schema({
                'type': 'str',
                'required': True
            })
        })

    For a complete list of :class:`OnticProperty` settings, see
    :ref:`property-schema-settings-table`.
    """

    def __init__(self, *args, **kwargs):

        # Detect if the list is a list of dicts or OnticProperty types.
        schema_list = None
        if len(args) == 1 and isinstance(args[0], list):
            if len(args[0]) > 0 and isinstance(args[0][0], dict):
                schema_list = args[0]

        if schema_list:
            super(Schema, self).__init__()
            for some_property in schema_list:
                self.add(some_property)
            return  # Initialization completed for a list.

        super(Schema, self).__init__(*args, **kwargs)

        for key, value in self.items():
            if not isinstance(value, property.OnticProperty):
                try:
                    if isinstance(value, dict):
                        value['name'] = key  # Set name for consistency.
                    self[key] = property.OnticProperty(value)
                except Exception:
                    logging.exception(
                        'Exception while converting "%s" to OnticProperty', key)
                    raise

    def add(self,
            property_type: Union[dict, property.OnticProperty]) -> None:
        """

        :param property_type:
        :type property_type: [dict, ontic_property.OnticProperty]
        """
        if not isinstance(property_type, (dict, property.OnticProperty)):
            raise ValueError(
                '"property_type" must be dict or OnticProperty type.')
        if isinstance(property_type, property.OnticProperty):
            self[property_type.name] = property_type

        else:
            ontic_prop = property.OnticProperty(property_type)
            self[ontic_prop.name] = ontic_prop

    def perfect(self) -> None:
        """Method to clean and perfect a given schema.

        The *perfect* will fill in any missing schema settings for each of
        the :class:`OnticProperty`. This function should be used to ensure
        property schema completeness.

        :rtype: None
        """
        perfect_schema(self)

    def validate(self, raise_validation_exception: bool = True) -> List[str]:
        """Validate a given :class:`Schema`.

        This method will iterate through all of the
        :class:`OnticProperty` and validate that each definition is valid.
        The method will collect all of the errors and return those as a list
        of strings or raise a
        :class:`ontic.validation_exception.ValidationException`. The switch in
        behavior is determined by the *raise_validation_exception*

        :param raise_validation_exception: If True, then *validate_schema* will
            throw a *ValidationException* upon validation failure. If False,
            then a list of validation errors is returned. Defaults to True.
        :type raise_validation_exception: bool
        :return: List of errors found. Empty of no errors found.
        :rtype: list<str>
        :raises ValueError: *candidate_schema* is None, or not of type
            :class:`Schema`.
        :raises ValidationException: A property of *candidate_schema* does not
            meet schema requirements.
        """
        return validate_schema(self, raise_validation_exception)


def perfect_schema(ontic_schema: Schema) -> None:
    """Method to clean and perfect a given schema.

    The *perfect_schema* will fill in any missing schema setting for each of
    the :class:`OnticProperty`. This function should be used to ensure
    property schema completeness.

    :param ontic_schema: The schema that is to be perfected.
    :type ontic_schema: :class:`Schema`
    :rtype: None
    """
    if ontic_schema is None:
        raise ValueError('"ontic_schema" must be provided.')
    if not isinstance(ontic_schema, Schema):
        raise ValueError('"ontic_schema" argument must be of Schema type.')

    [property_schema.perfect() for property_schema in ontic_schema.values()]


def validate_schema(
        ontic_schema: Schema,
        raise_validation_exception: bool = True) -> List[str]:
    """Validate a given :class:`Schema`.

    This method will iterate through all of the :class:`OnticProperty` and
    validate that each definition is valid.  The method will collect all of
    the errors and return those as a list of strings or raise a
    :class:`ontic.validation_exception.ValidationException`. The switch in
    behavior is determined by the *raise_validation_exception*

    :param ontic_schema: The schema to be validated.
    :type ontic_schema: :class:`Schema`
    :param raise_validation_exception: If True, then *validate_schema* will
        throw a *ValidationException* upon validation failure. If False, then a
        list of validation errors is returned. Defaults to True.
    :type raise_validation_exception: bool
    :return: List of errors found. Empty of no errors found.
    :rtype: list<str>
    :raises ValueError: *ontic_schema* is None, or not of type
        :class:`Schema`.
    :raises ValidationException: A property of *ontic_schema* does not
        meet schema requirements.
    """
    if ontic_schema is None:
        raise ValueError('"ontic_schema" argument must be provided.')
    if not isinstance(ontic_schema, Schema):
        raise ValueError('"ontic_schema" argument must be of Schema type.')

    value_errors = []
    for prop in ontic_schema.values():
        value_errors.extend(
            prop.validate(raise_validation_exception=False))

    if value_errors and raise_validation_exception:
        raise ValidationException(value_errors)

    return value_errors
