"""The classes utilized to construct schemas for object definitions.

.. image:: images/schema_type.jpg

.. contents::

======
Usage
======

The *schema_type* module contains the class :class:`SchemaType` and a set of
functions to create and validate schema. *SchemaType* are used to validate
:class:`ontic.ontic_type.OnticType` derived instances.

Creating Schema
----------------

A *SchemaType* is defined as a dictionary with the key entry being the name
of the property. The value portion of the dictionary is a
:class:`ontic.meta_type.PropertySchema` instance::

    >>> a_schema = SchemaType({
    ...     'property_name': PropertySchema({'type': 'str'})
    ... })

While the example above give a strict definition of a schema, creation of a
schema can omit the use of the *PropertySchema*, as the *SchemaType*
instantiation will convert a dict value to a *PropertySchema* object. The
above example can be simplified to be::

    >>> a_schema = SchemaType({
    ...     'property_name': {'type': 'str'}
    ... })

The *SchemaType* also supports the dict style of instantiation via parameter
naming::

    >>> a_schema = SchemaType(property_name={'type': 'str'})

Dynamic Schema
-----------------

In cases where necessary, a *SchemaType* can be created dynamically::

    >>> a_schema = SchemaType()
    >>> a_schema['property_name'] = PropertySchema({'type': 'str'})

To aid in the handling of dynamic models, utilize the :meth:`perfect_schema`
and :meth:`validate_schema`.

    >>> perfect_schema(a_schema)
    >>> errors = validate_schema(a_schema)

"""
from ontic import meta_type
from ontic.meta_type import CoreType, PropertySchema
from ontic.validation_exception import ValidationException


class SchemaType(CoreType):
    """The type definition for a schema object.

    The **SchemaType** contains a dictionary of property field names and
    the corresponding **PropertySchema** definition.

    Example SchemaType representation::

        SchemaType({
          'some_property': PropertySchema({
                'type': 'str',
                'required': True
            })
        })

    For a complete list of :class:`ontic.meta_type.PropertySchema`, see
    :ref:`property-schema-settings-table`.
    """

    def __init__(self, *args, **kwargs):
        r"""Initializes in accordance with dict specification.

        Dict Style Initialization
            *SchemaType* supports dict style initialization.

            SchemaType() -> new empty SchemaType

            SchemaType(mapping) -> new SchemaType initialized from a mapping
            object's (key, value) pairs

            SchemaType(iterable) -> new SchemaType initialized as if via::

                d = SchemaType()
                for k, v in iterable:
                    d[k] = v

            SchemaType(\*\*kwargs) -> new SchemaType initialized with the
            name=value pairs in the keyword argument list.  For example::

                SchemaType(one={. . .}, two={. . .})
        """
        super(SchemaType, self).__init__(*args, **kwargs)
        for key, value in self.iteritems():
            if not isinstance(value, PropertySchema):
                self[key] = PropertySchema(value)


def perfect_schema(candidate_schema):
    """Method to clean and perfect a given schema.

    The *perfect_schema* will fill in any missing schema setting for each of
    the :class:`ontic.meta_type.PropertySchema`. This function should be used
    to ensure property schema completeness.

    :param candidate_schema: The schema that is to be perfected.
    :type candidate_schema: :class:`ontic.schema_type.SchemaType`
    :rtype: None
    """
    if candidate_schema is None:
        raise ValueError('"candidate_schema" must be provided.')
    if not isinstance(candidate_schema, SchemaType):
        raise ValueError('"candidate_schema" must be of SchemaType.')

    for property_schema in candidate_schema.values():
        meta_type.perfect_property_schema(property_schema)


def validate_schema(candidate_schema, raise_validation_exception=True):
    """Validate a given :class:`SchemaType`.

    This method will iterate through all of the
    :class:`ontic.meta_type.PropertySchema` and validate that each definition
    is valid.  The method will collect all of the errors and return those as
    a list of strings or raise a
    :class:`ontic.validation_exception.ValidationException`. The switch in
    behavior is determined by the *raise_validation_exception*

    :param candidate_schema: The schema to be validated.
    :type candidate_schema: :class:`SchemaType`
    :param raise_validation_exception: If True, then *validate_schema* will
        throw a *ValidationException* upon validation failure. If False, then a
        list of validation errors is returned. Defaults to True.
    :type raise_validation_exception: bool
    :return: If no validation errors are found, then *None* is
        returned. If validation fails, then a list of the errors is returned,
        if the *raise_value_error* is not set to True.
    :rtype: list<str>, None
    :raises ValueError: *candidate_schema* is None, or not of type
        :class:`SchemaType`.
    :raises ValidationException: A property of *candidate_schema* does not
        meet schema requirements.
    """
    if candidate_schema is None:
        raise ValueError('"candidate_schema" must be provided.')
    if not isinstance(candidate_schema, SchemaType):
        raise ValueError('"candidate_schema" must be of SchemaType.')

    value_errors = []
    for candidate_property_schema in candidate_schema.values():
        value_errors.extend(
            meta_type.validate_property_schema(
                candidate_property_schema, False))

    if value_errors:
        if raise_validation_exception:
            raise ValidationException(value_errors)
        else:
            return value_errors
    else:
        return None
