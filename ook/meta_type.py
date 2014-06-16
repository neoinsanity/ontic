"""The base class for deriving types that require schema support.


.. image:: images/metadata_types.jpg

Usage
------
"""

from datetime import date, datetime, time
import re

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

    **CoreType** ensures that *Ook* objects can be access by either dict key
    or object attribute.

    :Example:

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
        dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)

        :param seq: Args to be passed to `dict` parent class.
        :param kwargs: Named args to be passed to `dict` parent class.
        """
        super(CoreType, self).__init__(*args, **kwargs)

        self.__dict__ = self


class MetaType(CoreType):
    # : The Ook schema pointer.
    OOK_SCHEMA = None

    @classmethod
    def get_schema(cls):
        """Returns the **SchemaType** instance for a given **Ook** type.

        :return: The schema metadata definition for the BaseType derived
            child type.
        :rtype: ook.object_type.SchemaType.
        """
        return cls.OOK_SCHEMA


class SchemaProperty(MetaType):
    """The object type for representing Property schema definitions.

    **Property Schema Settings**
        type
            :Value Options: bool, date, datetime, dict, float, int, list, None,
                set, str, time
            :Default: to None.

        required
            :Value Options: True, False
            :Default: False

        default
            :Value Options: The default is only restricted to the *type*
                setting, if a type has been set. If no *type* as been set,
                then default may be any value.
            :Default: None

        min
            :Value Options: int, float.
            :Default: None

        max
            :Value Options: int, float.
            :Default: None

        regex
            :Value Options: string.
            :Default: None

        member_type
            :Value Options: bool, date, datetime, dict, float, int, list, None,
                set, str, time
            :Default: None

        member_min
            :Value Options: int, float.
            :Default: None

        member_max
            :Value Options: int, float
            :Default: None

    """
    # The schema definition for the **SchemaProperty** type.
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

        dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)
        """
        super(SchemaProperty, self).__init__(*args, **kwargs)

        SchemaProperty.perfect_schema_property(self)

        value_errors = list()
        SchemaProperty.validate_schema_property(self, value_errors)
        if value_errors:
            raise ValueError(str.join(' \n-- ', value_errors))

    @staticmethod
    def validate_schema_property(candidate_schema_property, value_errors):
        """Method to validate a schema property definition.

        :param candidate_schema_property: The schema property to be validated.
        :type candidate_schema_property: ook.metadata_type.SchemaProperty
        :param value_errors: A list that is utilized to collect the errors found
            during schema validation.
        :type value_errors: list<str>
        :rtype: None
        """
        if candidate_schema_property is None:
            raise ValueError('"candidate_schema_property" must be provided.')
        if not isinstance(candidate_schema_property, SchemaProperty):
            raise ValueError(
                '"candidate_schema_property" must be SchemaProperty type.')

        for schema_name, schema_setting in (
                candidate_schema_property.get_schema().iteritems()):
            setting_value = candidate_schema_property.get(schema_name, None)

            SchemaProperty.validate_value(
                schema_name,
                schema_setting,
                setting_value,
                value_errors)

    @staticmethod
    def perfect_schema_property(candidate_schema_property):
        """Method to ensure the completeness of a given schema property.

        This method ensures completeness by stripping out any properties that
        are not defined by the schema definition. In addition, for any schema
        properties that are not included, the method will add those
        properties to the default value.

        :param candidate_schema_property:
        :rtype: None
        :raise: ValueError: If the candidate_schema_property is None, or not
            of type *SchemaProperty*.
        """
        if candidate_schema_property is None:
            raise ValueError('"candidate_schema_property" must be provided.')
        if not isinstance(candidate_schema_property, SchemaProperty):
            raise ValueError(
                '"candidate_schema_property" must be SchemaProperty type.')

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
        :type property_schema: meta_type.SchemaProperty
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
            SchemaProperty.validate_non_none_value(
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
        :type property_schema: ook.metadata_type.SchemaProperty
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
            if not SchemaProperty.enum_validation(property_schema, value):
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
                SchemaProperty.validate_collection_members(
                    key, property_schema, value, value_errors)
            else:
                if not SchemaProperty.enum_validation(property_schema, value):
                    value_errors.append(
                        'The value "%s" for "%s" not in enumeration %s.' %
                        (value, key, list(property_schema.enum)))
                    return  # No further processing can occur

                SchemaProperty.non_none_singular_validation(
                    key, property_schema, value, value_errors)

    @staticmethod
    def validate_collection_members(key, property_schema, value, value_errors):
        """Method to validate the members of a collection.

        This method only operates on *list* and *set* collection types.

        :param key: The name of the collection property to validate.
        :type key: str
        :param property_schema: The property schema to utilize for validation.
        :type property_schema: ook.metadata_type.PropertySchema
        :param value: The collection whose members will be validated.
        :type value: list, set
        :param value_errors: A list of errors found for a given collection.
            If any members fail validation, the error condition will be
            listed in value_errors list.
        :type value_errors: list<str>
        :rtype: None
        """
        if not SchemaProperty.min_validation(property_schema, value):
            value_errors.append('The value of "%s" for "%s" fails min of %s.' %
                                (value, key, property_schema.min))

        if not SchemaProperty.max_validation(property_schema, value):
            value_errors.append('The value of "%s" for "%s" fails max of %s.' %
                                (value, key, property_schema.max))

        if property_schema.type in {'list', 'set'}:
            validators = list()

            if property_schema.enum:
                validators.append(SchemaProperty.validate_member_enum)
            if property_schema.member_type:
                validators.append(SchemaProperty.validate_member_type)
            if property_schema.regex and property_schema.member_type == 'str':
                validators.append(SchemaProperty.validate_member_regex)
            if property_schema.member_min:
                validators.append(SchemaProperty.validate_member_min)
            if property_schema.member_max:
                validators.append(SchemaProperty.validate_member_max)

            for member_value in value:
                SchemaProperty.execute_collection_validators(
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
        :type property_schema: ook.metadata_type.PropertySchema
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
        :type property_schema: ook.metadata_type.PropertySchema
        :param value_errors: A list of errors found for a given value. If the
            validate fails, then an error message is added to the
            value_errors list.
        :type value_errors: list<str>
        :rtype: None
        """
        if not SchemaProperty.enum_validation(property_schema, member_value):
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
        :type property_schema: ook.metadata_type.PropertySchema
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
        :type property_schema: ook.metadata_type.SchemaProperty
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
        :type property_schema: ook.metadata_type.SchemaProperty
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
        :type property_schema: ook.metadata.PropertySchema
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
        :type property_schema: ook.metadata_type.PropertySchema
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
        :type property_schema: ook.metadata_type.PropertySchema
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
        :type property_schema: ook.metadata_type.PropertySchema
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
        :type property_schema: ook.meta_type.PropertySchema
        :param value: The value to be tested against the given schema.
        :type value: str, int, float, date, datetime, time, dict, list, set
        :param value_errors: A list of the validation errors discovered. The
            value errors will be added to if the given value fails validation.
        :type value_errors: list<str>
        :rtype: None
        """
        # min
        if not SchemaProperty.min_validation(property_schema, value):
            value_errors.append('The value of "%s" for "%s" fails min of %s.' %
                                (value, key, property_schema.min))

        # max
        if not SchemaProperty.max_validation(property_schema, value):
            value_errors.append('The value of "%s" for "%s" fails max of %s.' %
                                (value, key, property_schema.max))

        # regex validation
        if property_schema.regex:
            if property_schema.type == 'str' and value is not '':
                if not re.match(property_schema.regex, value):
                    value_errors.append(
                        'Value "%s" for %s does not meet regex: %s' %
                        (value, key, property_schema.regex))
