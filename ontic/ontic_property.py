"""The base class for deriving types that require schema support.


.. image:: images/property_type.jpg

.. contents::

======
Usage
======

The **meta_type** module contains three classes that are used in the
definition and instantiation of object instances.  The root class is
:class:`CoreType`, which is derived from the Python :class:`dict`. The
primary feature of the :class:`CoreType` is provide the means to access
properties of an object as a *dict* key or as object attribute.

Derived from :class:`CoreType` is :class:`MetaType`, which provides the
interface for retrieving a schema from an object schema definition via the
:meth:`MetaType.get_schema()`.

The :class:`PropertySchema` is utilized to define a schema for a single
property. This includes setting data type, required, and other such common
schema definition conventions. See :ref:`property-schema-settings-table` for
details on the :class:`PropertySchema` settings available.

It would be a rare case that requires the use of :class:`CoreType` or
:class:`MetaType`. For the majority of cases, the use of
:class:`PropertySchema` is sufficient. With that in mind, the remainder of
this section will focus on the use of :class:`PropertySchema`

Creating Property Schema
-------------------------

For general purposes, consider utilizing :class:`ontic.schema_type.SchemaType`,
for defining complete models. However, if you need validators for individual
properties, then direct use of :class:`PropertySchema` is a solution.

There are a number of ways to create a :class:`PropertySchema`. Take a look
at :class:`PropertySchema` class documentation for a complete exposition on
the means of instantiating an instance.

The most straight forward way to create an instance of a
:class:`PropertySchema`:

>>> prop_schema = PropertyType(type='str', required=True, min=3)
>>> assert prop_schema == {'regex': None, 'enum': None, 'min': 3, 'default': None, 'max': None,
...     'required': True, 'member_type': None, 'member_min': None,
...     'type': str, 'member_max': None}

Demonstrated above is the creation of a property schema of type string. In
addition the property schema forces the value of the property to required and
of minimum length of 3.

Along with the schema settings explicitly set in the constructor, there are a
number of other property schema settings that may be utilized. These
additional settings can be viewed in the output of the *prop_schema* object.
For the details on the property schema settings, see
:ref:`property-schema-settings-table`.

A :class:`PropertySchema` can be created or modified dynamically. If done so,
then the final schema instance should be validated with the use of the method
:meth:`validate_property_schema`.

Utilizing Property Schema
--------------------------

Validation of a value utilizing the *prop_schema* created, is done with the
:meth:`validate_value` method.

>>> prop_schema = PropertyType(type='str', required=True)
>>> some_value = 'The cat is on the roof.'
>>> validate_value(
...     name='some_value', property_schema=prop_schema, value=some_value)
[]

:class:`validate_value` returns an empty list if there are no errors.

The *name* parameter of the :meth:`validate_value`, is used to construct
friendly error messages. For example:

>>> validate_value('some_prop', prop_schema, None)
['The value for "some_prop" is required.']

The following example demonstrates how a :class:`PropertySchema` being
instantiated with a dictionary. Subsequently a bad value is passed with
multiple validation errors.

>>> other_schema = PropertyType({
...     'type': 'str',
...     'max': 3,
...     'enum': {'fish', 'dog', 'cat'}
... })
>>> ret = validate_value('other_prop', other_schema, 'frog')
>>> assert len(ret) == 2
>>> assert ret[0] == '''The value "frog" for "other_prop" not in enumeration ['cat', 'dog', 'fish'].'''
>>> assert ret[1] == '''The value of "frog" for "other_prop" fails max of 3.'''

.. _property-schema-settings-table:

Available Property Schema Settings
-----------------------------------

The following table gives a listing of the property schema settings that can
be used to define properties. Details on the schema settings are provided
after the table.

.. table:: Property Schema Settings

    ============ ========= ======== ========  =================================
    Name         Type      Default  Required  Enumeration
    ============ ========= ======== ========  =================================
    type         str       None     False     bool, complex, date,
                 type                         datetime, dict, float, int, list,
                                              None, set, str, time
    default      None      None     False
    required     bool      False    False
    enum         set       None     False
    min          complex   None     False
                 date
                 datetime
                 float
                 int
                 time
    max          complex   None     False
                 date
                 datetime
                 float
                 int
                 time
    regex        str       None     False
    member_type  str       None     False     bool, complex, date,
                 type                         datetime, dict, float, int, list,
                                              None, set, str, time
    member_min   complex   None     False
                 date
                 datetime
                 float
                 int
                 time
    member_max   complex   None     False
                 date
                 datetime
                 float
                 int
                 time
    ============ ========= ======== ========  =================================

*type*
    The *type* settings restricts a property to a known type. If no type is
    defined, then any value type may be assigned to the property.

    The type definition can be by type or by string name. Both ``{type=int}``
    and ``{type='int'}`` are valid examples of type declaration.
*default*
    If no default is applied, then the default value will be ``None``. If a
    default value is supplied, it will only be applied under two conditions.
    A default value is applied during instantiation of an object of type
    :class:`PropertySchema`, :class:`~ontic.schema_type.SchemaType`,
    or :class:`~ontic.ontic_type.OnticType`. The other case is when an
    instance of on of the given types is perfected via the methods
    :func:`perfect_property_schema`, :func:`~ontic.schema_type.perfect_schema`,
    or :func:`~ontic.ontic_type.perfect_object`.

    The default is not applied during validation.

    For the collection types (dict, list, and set), the default value is deep
    copied. This is done to ensure that there is no sharing of collection
    instances or values.
*required*
    A *PropertySchema* with a required setting of *True*, will fail
    validation if the property value is *None*.
*enum*
    An *enum* setting is a set of values that the property value must adhere
    to. If the *type* setting is provided, then the choices provided by
    *enum* must be of that type. If no *type* is provided, then the choices
    in the *enum* set may be of any type, even mixed type.
*min*
    The *min* setting has differing behavior, based on the *type* setting. If
    no *type* setting is provided, then *min* test will not occur. For the
    boundable types (strings and collections) the *min* setting will test that
    the value length is not less than the minimum. For the comparable types
    (numeric and chronological) the *min* setting will test that the
    value is not less than the minimum.
*max*
    The *max setting has differing behavior, based on the *type* setting. If
    no *type* setting is provided, the *max* test will not occur. For the
    boundable types (strings and collections) the *max* setting will test that
    the value length is not more than the maximum. For the comparable types
    (numeric and chronological) the *max* setting will test that the
    value is not more than the maximum.
*regex*
    The *regex* setting is only tested if the *type* or *member_type* setting
    is 'str' and the *regex* setting is not None. When active, the *regex*
    setting will be used to test the given string value.  If the property
    value is 'None', then no regex testing will be done.
*member_type*
    The *member_type* setting is used to restrict the value type for property
    *type* 'list' or 'set'. It does so ensuring that each member of the
    collection is of the type designated by *member_type*.

    The type definition can be by type or by string name. Both
    ``{member_type=int}`` and ``{member_type='int'}`` are valid examples of
    type declaration.
*member_min*
    The *member_min* setting has differing behavior, based on the
    *member_type* setting. If no *member_type* setting is provided, then
    *member_min* test will not occur. For the boundable types
    (strings and collections), the *member_min* setting will test that the
    value length is not less than the minimum. For the comparable types
    (numeric and chronological) the *member_minimum* setting will test
    that the value is not less than the minimum.
*member_max*
    The *member_max* setting has differing behavior, based on the
    *member_max* setting. If no *member_type* setting is provided,
    then *member_max* test will not occur. For the boundable types
    (strings and collections), the *member_max* setting will test that the
    value length is not more than the maximum. For the comparable types
    (numeric and chronological) the *member_max* setting will test
    that the value is not more than the maximum.

"""
from typing import List

from ontic import ontic_meta
from ontic import validation_exception


class OnticProperty(ontic_meta.OnticMeta):
    """A class to define a schema for a property."""

    def __init__(self, *args, **kwargs):
        super(OnticProperty, self).__init__(*args, **kwargs)

        self.perfect()
        self.validate()

    def perfect(self) -> None:
        """Method to ensure the completeness of a given schema property.

        :rtype: None
        :raises ValueError: If the candidate_property_type is None, or not
            of type *PropertyType*.
        """
        perfect_property(self)

    def validate(self, raise_validation_exception: bool = True) -> None:
        """Method to validate a property schema definition.

        :param raise_validation_exception: If True, then
            *validate_property_type* will throw a *ValueException* upon
            validation failure. If False, then a list of validation errors is
            returned. Defaults to True.
        :type raise_validation_exception: bool
        :return: If no validation errors are found, then *None* is returned.
            If validation fails, then a list of the errors is returned if the
            *raise_validation_exception* is set to True.
        :rtype: list<str>, None
        :raises ValueError: *the_candidate_schema_property* is not an
            :class:`OnticProperty`.
        :raises ValidationException: A property of *candidate_property_type*
            does not meet schema requirements.
        """
        return validate_property(self, raise_validation_exception)


def perfect_property(ontic_property: OnticProperty) -> None:
    """Method to ensure the completeness of a given schema property.

    This method ensures completeness by stripping out any properties that
    are not defined by the schema definition. In addition, for any schema
    properties that are not included, the method will add those
    properties to the default value.

    :param ontic_property: The OnticProperty that is to be clean and restricted.
    :type ontic_property: :class:`OnticProperty`
    :rtype: None
    :raises ValueError: If the ontic_property is None, or not of type
        *OnticProperty*.
    """
    if ontic_property is None:
        raise ValueError('"ontic_property" must be provided.')
    if not isinstance(ontic_property, OnticProperty):
        raise ValueError('"ontic_property" must be OnticProperty type.')

    property_schema = ontic_property.get_schema()

    # remove un-necessary properties.
    extra_properties = set(ontic_property.keys()) - set(property_schema.keys())
    for property_name in extra_properties:
        del ontic_property[property_name]

    if 'type' in ontic_property:
        _perfect_type_setting(ontic_property)
    else:
        ontic_property.type = None

    if 'member_type' in ontic_property:
        _perfect_member_type_setting(ontic_property)
    else:
        ontic_property.member_type = None

    # set the default for the given property.
    for property_name, property_schema in property_schema.items():
        if property_name not in ontic_property:
            ontic_property[property_name] = None
        if ontic_property[property_name] is None:
            ontic_property[property_name] = property_schema.default


def validate_property(
        ontic_property: OnticProperty,
        raise_validation_exception: bool = True) -> List[str]:
    """Method to validate a property schema definition.

    :param ontic_property: The schema property to be validated.
    :type ontic_property: :class:`OnticProperty`
    :param raise_validation_exception: If True, then *validate_property_type*
        will throw a *ValueException* upon validation failure. If False,
        then a list of validation errors is returned. Defaults to True.
    :type raise_validation_exception: bool
    :return: If no validation errors are found, then *None* is
        returned. If validation fails, then a list of the errors is returned
        if the *raise_validation_exception* is set to True.
    :rtype: list<str>, None
    :raises ValueError: *the_candidate_schema_property* is not an
        :class:`~ontic.ontic_type.OnticType`.
    :raises ValidationException: A property of *candidate_property_type*
        does not meet schema requirements.
    """
    if ontic_property is None:
        raise ValueError('"ontic_property" must be provided.')
    if not isinstance(ontic_property, OnticProperty):
        raise ValueError('"ontic_property" must be OnticProperty type.')

    value_errors = []

    for setting_name, setting_schema in ontic_property.get_schema().items():
        setting_value = ontic_property.get(setting_name, None)

        # todo: raul - for now skip validating compound schemas.
        if (isinstance(setting_value, type) and
                issubclass(setting_value, ontic_meta.OnticMeta)):
            continue

        value_errors.extend(
            ontic_meta.validate_value(
                setting_name, setting_schema, setting_value))

    if value_errors and raise_validation_exception:
        raise validation_exception.ValidationException(value_errors)

    return value_errors


def _perfect_type_setting(ontic_property: OnticProperty) -> None:
    """Perfect the type setting for a given candidate property schema."""
    if ontic_property.type is None:
        return

    candidate_type = ontic_property.type
    # coerce type declarations as string to base types.
    if isinstance(candidate_type, str):
        try:
            candidate_type = ontic_property.type = ontic_meta.TYPE_MAP[
                candidate_type]
        except KeyError:
            raise ValueError('Illegal type declaration: %s' %
                             ontic_property.type)

    # ensure that the type declaration is valid
    is_supported_type = candidate_type in ontic_meta.TYPE_SET
    is_meta_schema_type = issubclass(candidate_type, ontic_meta.OnticMeta)
    if not (is_supported_type or is_meta_schema_type):
        raise ValueError('Illegal type declaration: %s' % str(candidate_type))


def _perfect_member_type_setting(ontic_property: OnticProperty) -> None:
    """Perfect the member_type setting for a given candidate property schema."""
    if ontic_property.member_type is None:
        return

    candidate_type = ontic_property.member_type
    # coerce type declarations as string to base types.
    if isinstance(candidate_type, str):
        try:
            candidate_type = ontic_property.member_type = ontic_meta.TYPE_MAP[
                candidate_type]
        except KeyError:
            raise ValueError('Illegal member_type declaration: %s' %
                             ontic_property.member_type)

    # ensure that the type declaration is valid
    is_supported_type = candidate_type in ontic_meta.TYPE_SET
    is_meta_schema_type = issubclass(candidate_type, ontic_meta.OnticMeta)
    if not (is_supported_type or is_meta_schema_type):
        raise ValueError('Illegal type declaration: %s' % candidate_type)
