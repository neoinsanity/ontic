"""The base class for deriving types that require schema support.


.. image:: images/metadata_types.jpg

Usage
------

The **meta_type** module contains three classes that are used in the
definition and instantiation of object instances.  The root class is
:class:`CoreType`, which is derived from the Python :class:`dict`.

Derived from :class:`CoreType` is :class:`MetaType`, which provides the
interface for retrieving a schema from an object schema definition via the
:meth:`MetaType.get_schema()`.

The :class:`PropertySchema` is utilized to define a schema for a single
property. This includes setting data type, required, and other such common
schema definition conventions. See :ref:`property-schema-settings-table` for
details on the :class:`PropertySchema` settings available.

.. _property-schema-settings-table:

Property Schema Settings
-------------------------

Can this be the issue.

============ ====== ======== ========  =================================
name         type   default  required  enum
============ ====== ======== ========  =================================
type         str    None     False     bool, dict, float, int,
                                       list, set, str, date, , datetime
default      None   None     False     None
required     bool   False    False     None
enum         set    None     False     None
min          float  None     False     None
max          float  None     False     None
regex        str    None     False     None
member_type  str    None     False     bool, dict, float, int,
                                       list, set, str, date, , datetime
member_min   float  None     False     None
member_max   float  None     False     None
============ ====== ======== ========  =================================


"""

from datetime import date, datetime, time
import re

from validation_exception import ValidationException

# : The set of supported collection types.
COLLECTION_TYPES = {dict, list, set}

# : The set of types that can be compared with inequality operators.
COMPARABLE_TYPES = {'int', 'float', 'date', 'time', 'datetime'}

# : The set of types that may be limited in size.
BOUNDABLE_TYPES = {'str', 'list', 'dict', 'set'}

# : Used to convert the string declaration of attribute type to native type.
TYPE_MAP = {
    'bool': bool,
    'date': date,
    'datetime': datetime,
    'dict': dict,
    'float': float,
    'int': int,
    'list': list,
    'set': set,
    'str': basestring,
    'time': time,
}


class CoreType(dict):
    """The root type of *Ook* types.

    **CoreType** ensures that *Ook* object properties can be accessed by either
    dict key or object attribute. For example::

    >>> some_object = CoreType({'key1': 'value1'})
    >>> assert some_object.key1 == 'value1'
    >>> assert some_object['key1'] == 'value1'
    >>> some_object.key2 = 'value2'
    >>> assert some_object['key2'] == 'value2'
    >>> some_object['key3'] = 'value3'
    >>> assert some_object.key3 == 'value3'
    """

    def __init__(self, *args, **kwargs):
        """**CoreType** initialized as a `dict` type.

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
    """Interface for type definition of **Ook** schema defined classes.

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
    # : The Ook schema pointer.
    OOK_SCHEMA = None

    @classmethod
    def get_schema(cls):
        """Returns the schema object for the a given type definition.

        :return: The schema metadata definition for a :class:`PropertySchema`
            or a :class:`ook.object_type.ObjectType` derived child class.
        :rtype: :class:`CoreType`, :class:`ook.schema_type.SchemaType`
        """
        return cls.OOK_SCHEMA


class PropertySchema(MetaType):
    """The object type for representing Property schema definitions.

    The PropertySchema class is used to define individual properties of an
    object. For the complete set of property schema settings to define a
    property, see :ref:`property-schema-settings-table`

    Examples::

        There are a number of ways to create a PropertySchema for us in
        validation of a property. The most straight forward is to define
        create a property schema with a dictionary.

        >>> foo_schema = PropertySchema({
        ...     'type': 'str',
        ...     'required': True,
        ...     'default': 'Undefined',
        ... })

        PropertySchema also support the full range of dict style of
        instantiation.

        >>> boo_schema = PropertySchema([('type','str'),('required',True)])
        >>> moo_schema = PropertySchema(type='str', default='Cow')

        PropertySchema can also be assembled pragmatically.

        >>> bar_schema = PropertySchema()
        >>> bar_schema.type = 'int'
        >>> bar_schema.required = False
        >>> bar_schema.min = 3
        >>> val_errors = PropertySchema.validate_schema_property(bar_schema)
        >>> assert len(val_errors) == 0

        >>> nutty_schema = PropertySchema()
        >>> nutty_schema['type'] = 'str'
        >>> nutty_schema['required'] = True
        >>> nutty_schema['min'] = 5
        >>> val_errors = PropertySchema.validate_schema_property(nutty_schema)
        >>> assert len(val_errors) == 0
    """
    # : The schema definition for the **PropertySchema** type.
    OOK_SCHEMA = CoreType({
        'type': MetaType({
            'type': 'str',
            'default': None,
            'required': False,
            'enum': {
                'bool',
                'dict',
                'float',
                'int',
                'list',
                'set',
                'str',
                'date',
                'time',
                'datetime'},
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
            'type': 'bool',
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
            'type': 'set',
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
            'type': float,
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
            'type': float,
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
            'type': 'str',
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
            'type': 'str',
            'default': None,
            'required': False,
            'enum': {
                'bool',
                'dict',
                'float',
                'int',
                'list',
                'set',
                'str',
                'date',
                'time',
                'datetime',
            },
            'min': None,
            'max': None,
            'regex': None,
            'member_type': None,
            'member_min': None,
            'member_max': None,
        }),
        'member_min': MetaType({
            'type': float,
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
            'type': float,
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
        """Initializes in accordance with dict specification.

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

        PropertySchema.perfect_schema_property(self)

        PropertySchema.validate_schema_property(self)

    @staticmethod
    def validate_schema_property(candidate_schema_property,
                                 raise_value_error=True):
        """Method to validate a schema property definition.

        :param candidate_schema_property: The schema property to be validated.
        :type candidate_schema_property: :class:`PropertySchema`
        :return: If no validation errors are found, then an empty list is
            returned. If validation fails, then a list of the errors is returned
            if the *raise_value_error* is set to True.
        :rtype: list<str>
        :raises ValueError: *the_candidate_schema_property* is not an
            :class:`~ook.object_type.ObjectType`.
        :raises ValueError: A property of *candidate_schema_property* does not
            meet schema requirements.
        """
        if candidate_schema_property is None:
            raise ValueError('"candidate_schema_property" must be provided.')
        if not isinstance(candidate_schema_property, PropertySchema):
            raise ValueError(
                '"candidate_schema_property" must be PropertySchema type.')

        value_errors = list()

        for schema_name, schema_setting in (
                candidate_schema_property.get_schema().iteritems()):
            setting_value = candidate_schema_property.get(schema_name, None)

            PropertySchema.validate_value(
                schema_name,
                schema_setting,
                setting_value,
                value_errors)

        if value_errors and raise_value_error:
            raise ValidationException(value_errors)

        return value_errors

    @staticmethod
    def perfect_schema_property(candidate_schema_property):
        """Method to ensure the completeness of a given schema property.

        This method ensures completeness by stripping out any properties that
        are not defined by the schema definition. In addition, for any schema
        properties that are not included, the method will add those
        properties to the default value.

        :param candidate_schema_property: The PropertySchema that is to be
            clean and restricted.
        :type candidate_schema_property: :class:`PropertySchema`
        :rtype: None
        :raise: ValueError: If the candidate_schema_property is None, or not
            of type *PropertySchema*.
        """
        if candidate_schema_property is None:
            raise ValueError('"candidate_schema_property" must be provided.')
        if not isinstance(candidate_schema_property, PropertySchema):
            raise ValueError(
                '"candidate_schema_property" must be PropertySchema type.')

        schema_property_schema = candidate_schema_property.get_schema()

        extra_properties = set(candidate_schema_property.keys()) - set(
            schema_property_schema.keys())
        for property_name in extra_properties:
            del candidate_schema_property[property_name]

        for property_name, property_schema in (
                schema_property_schema.iteritems()):
            if property_name not in candidate_schema_property:
                candidate_schema_property[
                    property_name] = property_schema.default

    @staticmethod
    def validate_value(name, property_schema, value, value_errors):
        """Method to validate a given value against a given property schema.

        :param name: The name of the value to be validated.
        :type name: str
        :param property_schema: The property schema that contains the validation
            rules.
        :type property_schema: :class:`PropertySchema`
        :param value: The value that is to be validated.
        :type value: object
        :param value_errors: A list that is utilized to collect the errors found
            during schema validation.
        :type value_errors: list<str>
        """
        # required: True | False
        if property_schema.required and value is None:
            value_errors.append('The value for "%s" is required.' % name)
            return  # No other validation can occur without the required value

        if value is not None:
            PropertySchema.validate_non_none_value(
                name, property_schema, value, value_errors)

    @staticmethod
    def validate_non_none_value(key, property_schema, value, value_errors):
        """Validates an **Ook** object value that is not None.

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
        # Divide between single and collection types for validation processing.
        schema_value_type = TYPE_MAP.get(property_schema.type)

        if not schema_value_type:
            # if no schema_type, then just check that
            # the value is in an enum if necessary.
            if not PropertySchema.enum_validation(property_schema, value):
                value_errors.append(
                    'The value "%s" for "%s" not in enumeration %s.' %
                    (value, key, list(property_schema.enum)))
                return  # No further processing can occur
        else:
            # type checking
            if not isinstance(value, schema_value_type):
                value_errors.append(
                    'The value for "%s" is not of type "%s": %s' %
                    (key, property_schema.type, str(value)))
                return  # If not of the expected type, than can't further
                # validate without errors.

            if schema_value_type in COLLECTION_TYPES:
                PropertySchema.validate_collection_members(
                    key, property_schema, value, value_errors)
            else:
                if not PropertySchema.enum_validation(property_schema, value):
                    value_errors.append(
                        'The value "%s" for "%s" not in enumeration %s.' %
                        (value, key, list(property_schema.enum)))
                    return  # No further processing can occur

                PropertySchema.non_none_singular_validation(
                    key, property_schema, value, value_errors)

    @staticmethod
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
        if not PropertySchema.min_validation(property_schema, value):
            value_errors.append('The value of "%s" for "%s" fails min of %s.' %
                                (value, key, property_schema.min))

        if not PropertySchema.max_validation(property_schema, value):
            value_errors.append('The value of "%s" for "%s" fails max of %s.' %
                                (value, key, property_schema.max))

        if property_schema.type in {'list', 'set'}:
            validators = list()

            if property_schema.enum:
                validators.append(PropertySchema.validate_member_enum)
            if property_schema.member_type:
                validators.append(PropertySchema.validate_member_type)
            if property_schema.regex and property_schema.member_type == 'str':
                validators.append(PropertySchema.validate_member_regex)
            if property_schema.member_min:
                validators.append(PropertySchema.validate_member_min)
            if property_schema.member_max:
                validators.append(PropertySchema.validate_member_max)

            for member_value in value:
                PropertySchema.execute_collection_validators(
                    key,
                    member_value,
                    property_schema,
                    validators,
                    value_errors)

    @staticmethod
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

    @staticmethod
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
        if not PropertySchema.enum_validation(property_schema, member_value):
            value_errors.append(
                'The value "%s" for "%s" not in enumeration %s.' %
                (member_value, key, sorted(list(property_schema.enum))))

    @staticmethod
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
        schema_value_type = TYPE_MAP.get(
            property_schema.member_type)
        if not isinstance(member_value, schema_value_type):
            value_errors.append(
                'The value "%s" for "%s" is not of type "%s".' %
                (str(member_value), key, property_schema.member_type))

    @staticmethod
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

    @staticmethod
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
        if property_schema.member_type == 'str':
            if len(member_value) < property_schema.member_min:
                value_errors.append(
                    'The value of "%s" for "%s" fails min length of %s.' %
                    (member_value, key, property_schema.member_min))
        elif property_schema.member_type in COMPARABLE_TYPES:
            if member_value < property_schema.member_min:
                value_errors.append(
                    'The value of "%s" for "%s" fails min size of %s.' %
                    (member_value, key, property_schema.member_min))

    @staticmethod
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
        if property_schema.member_type == 'str':
            if len(member_value) > property_schema.member_max:
                value_errors.append(
                    'The value of "%s" for "%s" fails max length of %s.' %
                    (member_value, key, property_schema.member_max))
        elif property_schema.member_type in COMPARABLE_TYPES:
            if member_value > property_schema.member_max:
                value_errors.append(
                    'The value of "%s" for "%s" fails max size of %s.' %
                    (member_value, key, property_schema.member_max))

    @staticmethod
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

    @staticmethod
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
            elif property_schema.type in COMPARABLE_TYPES:
                if value < property_schema.min:
                    return False

        return True

    @staticmethod
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
            elif property_schema.type in COMPARABLE_TYPES:
                if value > property_schema.max:
                    return False

        return True

    @staticmethod
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
        # min
        if not PropertySchema.min_validation(property_schema, value):
            value_errors.append('The value of "%s" for "%s" fails min of %s.' %
                                (value, key, property_schema.min))

        # max
        if not PropertySchema.max_validation(property_schema, value):
            value_errors.append('The value of "%s" for "%s" fails max of %s.' %
                                (value, key, property_schema.max))

        # regex validation
        if property_schema.regex:
            if property_schema.type == 'str' and value is not '':
                if not re.match(property_schema.regex, value):
                    value_errors.append(
                        'Value "%s" for %s does not meet regex: %s' %
                        (value, key, property_schema.regex))
