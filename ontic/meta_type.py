"""The base class for deriving types that require schema support.


.. image:: images/metadata_types.jpg

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

>>> prop_schema = PropertySchema(type='str', required=True, min=3)
>>> prop_schema
{'regex': None, 'enum': None, 'min': 3, 'default': None, 'max': None, \
'required': True, 'member_type': None, 'member_min': None, \
'type': <type 'str'>, 'member_max': None}

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

>>> prop_schema = PropertySchema(type='str', required=True)
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

>>> other_schema = PropertySchema({
...     'type': 'str',
...     'max': 3,
...     'enum': {'dog', 'rat', 'cat'}
... })
>>> validate_value('other_prop', other_schema, 'frog')
['The value "frog" for "other_prop" not in enumeration [\\'rat\\', \\'dog\\', \
\\'cat\\'].', 'The value of "frog" for "other_prop" fails max of 3.']

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
    type         str       None     False     basestring, bool, complex, date,
                 type                         datetime, dict, float, int, list,
                                              long, None, set, str, time,
                                              unicode
    default      None      None     False
    required     bool      False    False
    enum         set       None     False
    min          complex   None     False
                 date
                 datetime
                 float
                 int
                 long
                 time
    max          complex   None     False
                 date
                 datetime
                 float
                 int
                 long
                 time
    regex        str       None     False
    member_type  str       None     False     basestring, bool, complex, date,
                 type                         datetime, dict, float, int, list,
                                              long, None, set, str, time,
                                              unicode
    member_min   complex   None     False
                 date
                 datetime
                 float
                 int
                 long
                 time
    member_max   complex   None     False
                 date
                 datetime
                 float
                 int
                 long
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

from datetime import date, datetime, time
import re

from ontic.validation_exception import ValidationException

# : The set of supported collection types.
COLLECTION_TYPES = {dict, list, set}

# : The set of types that can be compared with inequality operators.
COMPARABLE_TYPES = {complex, date, datetime, float, int, long, time}

# : The set of types that may be limited in size.
BOUNDABLE_TYPES = {basestring, str, unicode, list, dict, set}

# : The set of string types
STRING_TYPES = {basestring, str, unicode}

# : Used to convert the string declaration of attribute type to native type.
TYPE_MAP = {
    'basestring': basestring,
    basestring: basestring,
    'bool': bool,
    bool: bool,
    'complex': complex,
    complex: complex,
    'date': date,
    date: date,
    'datetime': datetime,
    datetime: datetime,
    'dict': dict,
    dict: dict,
    'float': float,
    float: float,
    'int': int,
    int: int,
    'list': list,
    list: list,
    'long': long,
    long: long,
    'None': None,
    None: None,
    'set': set,
    set: set,
    'str': str,
    str: str,
    'time': time,
    time: time,
    'unicode': unicode,
    unicode: unicode,
}


class CoreType(dict):
    """The root type of *Ontic* types.

    **CoreType** ensures that *Ontic* object properties can be accessed by
    either dict key or object attribute. For example::

    >>> some_object = CoreType({'key1': 'value1'})
    >>> assert some_object.key1 == 'value1'
    >>> assert some_object['key1'] == 'value1'
    >>> some_object.key2 = 'value2'
    >>> assert some_object['key2'] == 'value2'
    >>> some_object['key3'] = 'value3'
    >>> assert some_object.key3 == 'value3'
    """

    def __init__(self, *args, **kwargs):
        r"""**CoreType** initialized as a `dict` type.

        Initializes the accessor behavior to allow for property access as
        dict key or object attribute.

        Dict Style Initialization
            CoreType() -> new empty CoreType

            CoreType(mapping) -> new CoreType initialized from a mapping
            object's (key, value) pairs

            CoreType(iterable) -> new CoreType initialized as if via::

                d = CoreType()
                for k, v in iterable:
                    d[k] = v

            CoreType(\*\*kwargs) -> new CoreType initialized with the
            name=value pairs in the keyword argument list.  For example::

                CoreType(one=1, two=2)
        """
        super(CoreType, self).__init__(*args, **kwargs)

        self.__dict__ = self


class MetaType(CoreType):
    r"""Interface for type definition of **Ontic** schema defined classes.

    Dict Style Initialization
        MetaType() -> new empty MetaType

        MetaType(mapping) -> new MetaType initialized from a mapping object's
            (key, value) pairs

        MetaType(iterable) -> new MetaType initialized as if via::

            d = MetaType()
            for k, v in iterable:
                d[k] = v

        MetaType(\*\*kwargs) -> new MetaType initialized with the name=value
        pairs in the keyword argument list.  For example::

            MetaType(one=1, two=2)
    """
    # : The Ontic schema pointer.
    ONTIC_SCHEMA = None

    @classmethod
    def get_schema(cls):
        """Returns the schema object for the a given type definition.

        :return: The schema metadata definition for a :class:`PropertySchema`
            or a :class:`ontic.ontic_type.OnticType` derived child class.
        :rtype: :class:`CoreType`, :class:`ontic.schema_type.SchemaType`
        """
        return cls.ONTIC_SCHEMA


class PropertySchema(MetaType):
    """The object type for representing Property schema definitions.

    The PropertySchema class is used to define individual properties of an
    object. For the complete set of property schema settings to define a
    property, see :ref:`property-schema-settings-table`

    Examples::

        There are a number of ways to create a PropertySchema for use in
        validation of a property. The most straight forward is to define
        a property schema with a dictionary.

        >>> foo_schema = PropertySchema({
        ...     'type': 'str',
        ...     'required': True,
        ...     'default': 'Undefined',
        ... })

        PropertySchema also support the full range of dict style instantiation.

        >>> boo_schema = PropertySchema([('type','str'),('required',True)])
        >>> moo_schema = PropertySchema(type='str', default='Cow')

        PropertySchema can also be assembled pragmatically.

        >>> bar_schema = PropertySchema()
        >>> bar_schema.type = 'int'
        >>> bar_schema.required = False
        >>> bar_schema.min = 3
        >>> val_errors = validate_property_schema(bar_schema)
        >>> assert val_errors == []

        >>> nutty_schema = PropertySchema()
        >>> nutty_schema['type'] = 'str'
        >>> nutty_schema['required'] = True
        >>> nutty_schema['min'] = 5
        >>> val_errors = validate_property_schema(nutty_schema)
        >>> assert val_errors == []
    """
    # The schema definition for the **PropertySchema** type.
    ONTIC_SCHEMA = CoreType({
        'type': MetaType({
            'type': (basestring, str, unicode, type),
            'default': None,
            'required': False,
            'enum': set(TYPE_MAP.keys()),
            'min': None,
            'max': None,
            'regex': None,
            'member_type': None,
            'member_min': None,
            'member_max': None,
        }),
        'default': MetaType({
            'type': None,
            'default': None,
            'required': False,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'member_type': None,
            'member_min': None,
            'member_max': None,
        }),
        'required': MetaType({
            'type': bool,
            'default': False,
            'required': False,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'member_type': None,
            'member_min': None,
            'member_max': None,
        }),
        'enum': MetaType({
            'type': set,
            'default': None,
            'required': False,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'member_type': None,
            'member_min': None,
            'member_max': None,
        }),
        'min': MetaType({
            'type': tuple(COMPARABLE_TYPES),
            'default': None,
            'required': False,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'member_type': None,
            'member_min': None,
            'member_max': None,
        }),
        'max': MetaType({
            'type': tuple(COMPARABLE_TYPES),
            'default': None,
            'required': False,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'member_type': None,
            'member_min': None,
            'member_max': None,
        }),
        'regex': MetaType({
            'type': (basestring, str, unicode),
            'default': None,
            'required': False,
            'enum': None,
            'min': 1,
            'max': None,
            'regex': None,
            'member_type': None,
            'member_min': None,
            'member_max': None,
        }),
        'member_type': MetaType({
            'type': (basestring, str, unicode, type),
            'default': None,
            'required': False,
            'enum': set(TYPE_MAP.keys()),
            'min': None,
            'max': None,
            'regex': None,
            'member_type': None,
            'member_min': None,
            'member_max': None,
        }),
        'member_min': MetaType({
            'type': tuple(COMPARABLE_TYPES),
            'default': None,
            'required': False,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'member_type': None,
            'member_min': None,
            'member_max': None,
        }),
        'member_max': MetaType({
            'type': tuple(COMPARABLE_TYPES),
            'default': None,
            'required': False,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'member_type': None,
            'member_min': None,
            'member_max': None,
        }),
    })

    def __init__(self, *args, **kwargs):
        r"""Initializes in accordance with dict specification.

        PropertySchema initialization can be done with a Dict object or with
        None. A PropertySchema defined with None is legal and valid. It is
        therefore possible to define a property with no restrictions to
        assignment or requirement.

        Dict Style Initialization
            *PropertySchema* supports dict style initialization.

            PropertySchema() -> new empty PropertySchema

            PropertySchema(mapping) -> new PropertySchema initialized from a
            mapping object's (key, value) pairs

            PropertySchema(iterable) -> new PropertySchema initialized as if
            via::

                d = PropertySchema()
                for k, v in iterable:
                    d[k] = v

            PropertySchema(\*\*kwargs) -> new PropertySchema initialized with
            the name=value pairs in the keyword argument list.  For example::

                PropertySchema(one=1, two=2)
        """
        super(PropertySchema, self).__init__(*args, **kwargs)

        perfect_property_schema(self)

        validate_property_schema(self)


def validate_property_schema(candidate_property_schema,
                             raise_validation_exception=True):
    """Method to validate a property schema definition.

    :param candidate_property_schema: The schema property to be validated.
    :type candidate_property_schema: :class:`PropertySchema`
    :param raise_validation_exception: If True, then *validate_property_schema*
        will throw a *ValueException* upon validation failure. If False,
        then a list of validation errors is returned. Defaults to True.
    :type raise_validation_exception: bool
    :return: If no validation errors are found, then *None* is
        returned. If validation fails, then a list of the errors is returned
        if the *raise_validation_exception* is set to True.
    :rtype: list<str>, None
    :raises ValueError: *the_candidate_schema_property* is not an
        :class:`~ontic.ontic_type.OnticType`.
    :raises ValidationException: A property of *candidate_property_schema*
        does not meet schema requirements.
    """
    if candidate_property_schema is None:
        raise ValueError('"candidate_property_schema" must be provided.')
    if not isinstance(candidate_property_schema, PropertySchema):
        raise ValueError(
            '"candidate_property_schema" must be PropertySchema type.')

    value_errors = list()

    for schema_name, schema_setting in (
            candidate_property_schema.get_schema().iteritems()):
        setting_value = candidate_property_schema.get(schema_name, None)

        value_errors.extend(
            validate_value(schema_name, schema_setting, setting_value))

    if value_errors and raise_validation_exception:
        raise ValidationException(value_errors)

    return value_errors


def perfect_property_schema(candidate_property_schema):
    """Method to ensure the completeness of a given schema property.

    This method ensures completeness by stripping out any properties that
    are not defined by the schema definition. In addition, for any schema
    properties that are not included, the method will add those
    properties to the default value.

    :param candidate_property_schema: The PropertySchema that is to be
        clean and restricted.
    :type candidate_property_schema: :class:`PropertySchema`
    :rtype: None
    :raises ValueError: If the candidate_property_schema is None, or not
        of type *PropertySchema*.
    """
    if candidate_property_schema is None:
        raise ValueError('"candidate_property_schema" must be provided.')
    if not isinstance(candidate_property_schema, PropertySchema):
        raise ValueError(
            '"candidate_property_schema" must be PropertySchema type.')

    schema_property_schema = candidate_property_schema.get_schema()

    # remove un-necessary properties.
    extra_properties = set(candidate_property_schema.keys()) - set(
        schema_property_schema.keys())
    for property_name in extra_properties:
        del candidate_property_schema[property_name]

    if 'type' in candidate_property_schema:
        # ensure that the type declaration is valid
        if candidate_property_schema.type not in TYPE_MAP:
            raise ValueError('Illegal type declaration: %s' %
                             candidate_property_schema.type)
        # coerce type declarations as string to base types.
        candidate_property_schema.type = TYPE_MAP.get(
            candidate_property_schema.type, None)
    else:
        candidate_property_schema.type = None

    if 'member_type' in candidate_property_schema:
        # coerce member_type declarations as string to base types.
        candidate_property_schema.member_type = TYPE_MAP[
            candidate_property_schema.member_type]
    else:
        candidate_property_schema.member_type = None

    for property_name, property_schema in (
            schema_property_schema.iteritems()):
        if property_name not in candidate_property_schema:
            candidate_property_schema[
                property_name] = property_schema.default
            continue
        if not candidate_property_schema[property_name]:
            candidate_property_schema[property_name] = property_schema.default


def validate_value(name, property_schema, value):
    """Method to validate a given value against a given property schema.

    :param name: The name of the value to be validated.
    :type name: str
    :param property_schema: The property schema that contains the validation
        rules.
    :type property_schema: :class:`PropertySchema`
    :param value: The value that is to be validated.
    :type value: object
    :return: A list that is utilized to collect the errors found
        during schema validation.
    :rtype: list<str>
    """
    value_errors = []
    # required: True | False
    if property_schema.required and value is None:
        value_errors.append('The value for "%s" is required.' % name)
        return value_errors  # No other validation can occur without a value

    if value is not None:
        validate_non_none_value(name, property_schema, value, value_errors)

    return value_errors


def validate_non_none_value(key, property_schema, value, value_errors):
    """Validates an **Ontic** object value that is not None.

    This method validates singular and collection values. This method
    does not perform *Required* validation, as it is assumed that the
    value is not None.

    :param key: The name of the property to be validated.
    :type key: str
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`PropertySchema`
    :param value: The non-None value to be validated.
    :type value: object
    :param value_errors: A list of errors found for a given value. If any
        given validator method fails, it will append it error message to
        the value_errors list.
    :type value_errors: list<str>
    :rtype: None
    """
    if not property_schema.type:
        # if no schema_type, then just check that
        # the value is in an enum if necessary.
        if not enum_validation(property_schema, value):
            value_errors.append(
                'The value "%s" for "%s" not in enumeration %s.' %
                (value, key, list(property_schema.enum)))
            return  # No further processing can occur
    else:
        # type checking
        if not isinstance(value, property_schema.type):
            value_errors.append(
                'The value for "%s" is not of type "%s": %s' %
                (key, property_schema.type, str(value)))
            # If not of the expected type, than can't further
            # validate without errors.
            return

        if property_schema.type in COLLECTION_TYPES:
            validate_collection_members(
                key, property_schema, value, value_errors)
        else:
            non_none_singular_validation(
                key, property_schema, value, value_errors)


def validate_collection_members(key, property_schema, value, value_errors):
    """Method to validate the members of a collection.

    This method only operates on *list* and *set* collection types.

    :param key: The name of the collection property to validate.
    :type key: str
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`PropertySchema`
    :param value: The collection whose members will be validated.
    :type value: list, set
    :param value_errors: A list of errors found for a given collection.
        If any members fail validation, the error condition will be
        listed in value_errors list.
    :type value_errors: list<str>
    :rtype: None
    """
    if not min_validation(property_schema, value):
        value_errors.append('The value of "%s" for "%s" fails min of %s.' %
                            (value, key, property_schema.min))

    if not max_validation(property_schema, value):
        value_errors.append('The value of "%s" for "%s" fails max of %s.' %
                            (value, key, property_schema.max))

    if property_schema.type in {list, set}:
        validators = list()

        if property_schema.enum:
            validators.append(validate_member_enum)
        if property_schema.member_type:
            validators.append(validate_member_type)
        if property_schema.regex and property_schema.member_type == str:
            validators.append(validate_member_regex)
        if property_schema.member_min:
            validators.append(validate_member_min)
        if property_schema.member_max:
            validators.append(validate_member_max)

        for member_value in value:
            execute_collection_validators(
                key,
                member_value,
                property_schema,
                validators,
                value_errors)


def execute_collection_validators(
        key,
        member_value,
        property_schema,
        validators,
        value_errors):
    """Method to execute a list of validators on a given collection.

    :param key: The name of the collection property to validate.
    :type key: str
    :param member_value: The member of the collection property to validate.
    :type member_value: str, int, float, date, datetime, time
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`PropertySchema`
    :param validators: A list of validation methods to execute.
    :type validators: list<types.MethodType>
    :param value_errors: A list of errors found for a given value. If any
        given validator method fails, it will append it error message to
        the value_errors list.
    :type value_errors: list<str>
    :rtype: None
    """
    for validator in validators:
        validator(key, member_value, property_schema, value_errors)


def validate_member_enum(key, member_value, property_schema, value_errors):
    """Validate a member of a collection is within a defined enumeration.

    :param key: The name of the collection property to validate.
    :type key: str
    :param member_value: The member of the collection property to
        validate.
    :type member_value: str, int, float, date, datetime, time
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`PropertySchema`
    :param value_errors: A list of errors found for a given value. If the
        validate fails, then an error message is added to the
        value_errors list.
    :type value_errors: list<str>
    :rtype: None
    """
    if not enum_validation(property_schema, member_value):
        value_errors.append(
            'The value "%s" for "%s" not in enumeration %s.' %
            (member_value, key, sorted(list(property_schema.enum))))


def validate_member_type(key, member_value, property_schema, value_errors):
    """Validate a member of a collection is of a given type.

    :param key: The name of the collection property to validate.
    :type key: str
    :param member_value: The member value of the collection property to
        validate.
    :type member_value: object
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`PropertySchema`
    :param value_errors: A list of errors found for a given value. If the
        validation fails, then an error message is added to the
        value_errors list.
    :type value_errors: list<str>
    :rtype: None
    """
    if not isinstance(member_value, property_schema.member_type):
        value_errors.append(
            'The value "%s" for "%s" is not of type "%s".' %
            (str(member_value), key, property_schema.member_type))


def validate_member_regex(key, member_value, property_schema, value_errors):
    """Validate a member of a collection against a defined regex.

    :param key: The name of the collection property to validate.
    :type key: str
    :param member_value: The member value of the collection property to
        validate.
    :type member_value: str
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`PropertySchema`
    :param value_errors: A list of errors found for a given value. If the
        validation fails, then an error message is added to the
        value_errors list.
    :type value_errors: list<str>
    :rtype: None
    """
    if not re.match(property_schema.regex, member_value):
        value_errors.append(
            'Value "%s" for "%s" does not meet regex: %s' %
            (member_value, key, property_schema.regex))


def validate_member_min(key, member_value, property_schema, value_errors):
    """Validate a member of a collection for minimum allowable value.

    :param key: The name of the collection property to validate.
    :type key: str
    :param member_value: The member value of the collection property to
        validate.
    :type member_value: str, int, float, date, datetime, time
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`PropertySchema`
    :param value_errors: A list of errors found for a given value. If the
        validation fails, then an error message is added to the
        value_errors list.
    :type value_errors: list<str>
    :rtype: None
    """
    if property_schema.member_type in STRING_TYPES:
        if len(member_value) < property_schema.member_min:
            value_errors.append(
                'The value of "%s" for "%s" fails min length of %s.' %
                (member_value, key, property_schema.member_min))

    if property_schema.member_type in COMPARABLE_TYPES:
        if member_value < property_schema.member_min:
            value_errors.append(
                'The value of "%s" for "%s" fails min size of %s.' %
                (member_value, key, property_schema.member_min))


def validate_member_max(key, member_value, property_schema, value_errors):
    """Validate a member of a collection for maximum allowable value.

    :param key: The name of the collection property to validate.
    :type key: str
    :param member_value: The member value of the collection property to
        validate.
    :type member_value: str, int, float, date, datetime, time
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`PropertySchema`
    :param value_errors: A list of errors found for a given value. If the
        validation fails, then an error message is added to the
        value_errors list.
    :type value_errors: list<str>
    :rtype: None
    """
    if property_schema.member_type in STRING_TYPES:
        if len(member_value) > property_schema.member_max:
            value_errors.append(
                'The value of "%s" for "%s" fails max length of %s.' %
                (member_value, key, property_schema.member_max))

    if property_schema.member_type in COMPARABLE_TYPES:
        if member_value > property_schema.member_max:
            value_errors.append(
                'The value of "%s" for "%s" fails max size of %s.' %
                (member_value, key, property_schema.member_max))


def enum_validation(property_schema, value):
    """Validate a non-collection property for value in an enumeration set.

    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`PropertySchema`
    :param value: The value of the property to be validated.
    :type value: object
    :return: True if the validation is successful, else False.
    :rtype: bool
    """
    if property_schema.enum:
        if not value in property_schema.enum:
            return False
    return True


def min_validation(property_schema, value):
    """Validate a non-collection property for minimum allowable value.

    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`PropertySchema`
    :param value: The value of the property to be validated.
    :type value: str, int, float, date, datetime, time, dict, list, set
    :return: True if the validation is successful, else False.
    :rtype: bool
    """
    if property_schema.min:
        if property_schema.type in BOUNDABLE_TYPES:
            if len(value) < property_schema.min:
                return False
        if property_schema.type in COMPARABLE_TYPES:
            if value < property_schema.min:
                return False

    return True


def max_validation(property_schema, value):
    """Validates a non-collection property for maximum allowable value.

    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`PropertySchema`
    :param value: The value of the property to be validated.
    :type value: str, int, float, date, datetime, time, dict, list, set
    :return: True if the validation is successful, else False.
    :rtype: bool
    """
    if property_schema.max:
        if property_schema.type in BOUNDABLE_TYPES:
            if len(value) > property_schema.max:
                return False
        if property_schema.type in COMPARABLE_TYPES:
            if value > property_schema.max:
                return False

    return True


def non_none_singular_validation(key, property_schema, value, value_errors):
    """Method to validate an object value meets schema requirements.

    This method validates non-collection properties. The method should
    only be used for non-None values.

    :param key: The name of the property that is being validated.
    :type key: str
    :param property_schema: The schema definition for the target property.
    :type property_schema: :class:`PropertySchema`
    :param value: The value to be tested against the given schema.
    :type value: str, int, float, date, datetime, time, dict, list, set
    :param value_errors: A list of the validation errors discovered. The
        value errors will be added to if the given value fails validation.
    :type value_errors: list<str>
    :rtype: None
    """
    # enum
    if not enum_validation(property_schema, value):
        value_errors.append('The value "%s" for "%s" not in enumeration %s.' %
                            (value, key, list(property_schema.enum)))

    # min
    if not min_validation(property_schema, value):
        value_errors.append('The value of "%s" for "%s" fails min of %s.' %
                            (value, key, property_schema.min))

    # max
    if not max_validation(property_schema, value):
        value_errors.append('The value of "%s" for "%s" fails max of %s.' %
                            (value, key, property_schema.max))

    # regex validation
    if property_schema.regex:
        if property_schema.type in STRING_TYPES and value is not '':
            if not re.match(property_schema.regex, value):
                value_errors.append(
                    'Value "%s" for %s does not meet regex: %s' %
                    (value, key, property_schema.regex))
