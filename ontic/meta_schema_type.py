"""Class definition for a type that holds schema definitions.

.. image:: images/meta_type.jpg

.. contents::

"""
from datetime import date, datetime, time
import re
from typing import List, Any, Callable, Set, Tuple, TypeVar

from ontic.core_type import CoreType

#: The set of supported collection types.
COLLECTION_TYPES = {dict, list, set}

#: The set of types that can be compared with inequality operators.
COMPARABLE_TYPES = {complex, date, datetime, float, int, time}

#: The set of types that may be limited in size.
BOUNDABLE_TYPES = {str, list, dict, set}


class MetaSchemaType(CoreType):
    """Interface for type definition of **Ontic** schema defined classes.

    Dict Style Initialization
        MetaSchemaType() -> new empty MetaSchemaType

        MetaSchemaType(mapping) -> new MetaSchemaType initialized from a
        mapping object's (key, value) pairs

        MetaSchemaType(iterable) -> new MetaSchemaType initialized as if via::

            d = MetaSchemaType()
            for k, v in iterable:
                d[k] = v

        MetaSchemaType(\*\*kwargs) -> new MetaSchemaType initialized with the
        name=value pairs in the keyword argument list.  For example::

            MetaSchemaType(one=1, two=2)
    """
    #: The Ontic schema pointer.
    ONTIC_SCHEMA = None

    @classmethod
    def get_schema(cls) -> "MetaSchemaType":
        """Returns the schema object for the given type definition.

        :return: The schema metadata definition for a :class:`PropertyType`
            or a :class:`ontic.ontic_type.OnticType` derived child class.
        :rtype: :class:`ontic.schema_type.SchemaType`
        """
        return cls.ONTIC_SCHEMA


#: Used to convert the string declaration of attribute type to native type.
TYPE_MAP = {
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
    'None': None,
    None: None,
    MetaSchemaType: MetaSchemaType,
    'set': set,
    set: set,
    'str': str,
    str: str,
    'time': time,
    time: time,
}

TYPE_SET = (
    bool,
    complex,
    date,
    datetime,
    dict,
    float,
    int,
    list,
    set,
    str,
    time,
)


def validate_value(
        name: str,
        property_schema: MetaSchemaType,
        value: Any) -> List[str]:
    """Method to validate a given value against a given property schema.

    :param name: The name of the value to be validated.
    :type name: str
    :param property_schema: The property schema that contains the validation
        rules.
    :type property_schema: :class:`property_type.PropertyType`
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


def validate_non_none_value(
        key: str,
        property_schema: MetaSchemaType,
        value: Any, value_errors: List[str]) -> None:
    """Validates an **Ontic** object value that is not None.

    This method validates singular and collection values. This method
    does not perform *Required* validation, as it is assumed that the
    value is not None.

    :param key: The name of the property to be validated.
    :type key: str
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`property_type.PropertyType`
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
                (value, key, _generate_sorted_list(property_schema.enum)))
            return  # No further processing can occur.
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


def validate_collection_members(
        key: str,
        property_schema: MetaSchemaType,
        value: Any,
        value_errors: List[str]) -> None:
    """Method to validate the members of a collection.

    This method only operates on *list* and *set* collection types.

    :param key: The name of the collection property to validate.
    :type key: str
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`property_type.PropertyType`
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


#: Signature definition of a validator function.
ValidatorFunc = Callable[[str, Any, CoreType, List[str]], None]


def execute_collection_validators(
        key: str,
        member_value: Any,
        property_schema: MetaSchemaType,
        validators: List[ValidatorFunc],
        value_errors) -> None:
    """Method to execute a list of validators on a given collection.

    :param key: The name of the collection property to validate.
    :type key: str
    :param member_value: The member of the collection property to validate.
    :type member_value: str, int, float, date, datetime, time
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`property_type.PropertyType`
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


def validate_member_enum(
        key: str,
        member_value: Any,
        property_schema: MetaSchemaType,
        value_errors: List[str]) -> None:
    """Validate a member of a collection is within a defined enumeration.

    :param key: The name of the collection property to validate.
    :type key: str
    :param member_value: The member of the collection property to
        validate.
    :type member_value: str, int, float, date, datetime, time
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`property_type.PropertyType`
    :param value_errors: A list of errors found for a given value. If the
        validate fails, then an error message is added to the
        value_errors list.
    :type value_errors: list<str>
    :rtype: None
    """
    if not enum_validation(property_schema, member_value):
        value_errors.append(
            'The value "%s" for "%s" not in enumeration %s.' %
            (member_value, key, _generate_sorted_list(property_schema.enum)))


def validate_member_type(
        key: str,
        member_value: Any,
        property_schema: MetaSchemaType,
        value_errors: List[str]) -> None:
    """Validate a member of a collection is of a given type.

    :param key: The name of the collection property to validate.
    :type key: str
    :param member_value: The member value of the collection property to
        validate.
    :type member_value: object
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`property_type.PropertyType`
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


def validate_member_regex(
        key: str,
        member_value: Any,
        property_schema: MetaSchemaType,
        value_errors: List[str]) -> None:
    """Validate a member of a collection against a defined regex.

    :param key: The name of the collection property to validate.
    :type key: str
    :param member_value: The member value of the collection property to
        validate.
    :type member_value: str
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`property_type.PropertyType`
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


def validate_member_min(
        key: str,
        member_value: Any,
        property_schema: MetaSchemaType,
        value_errors: List[str]) -> None:
    """Validate a member of a collection for minimum allowable value.

    :param key: The name of the collection property to validate.
    :type key: str
    :param member_value: The member value of the collection property to
        validate.
    :type member_value: str, int, float, date, datetime, time
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`property_type.PropertyType`
    :param value_errors: A list of errors found for a given value. If the
        validation fails, then an error message is added to the
        value_errors list.
    :type value_errors: list<str>
    :rtype: None
    """
    if property_schema.member_type is str:
        if len(member_value) < property_schema.member_min:
            value_errors.append(
                'The value of "%s" for "%s" fails min length of %s.' %
                (member_value, key, property_schema.member_min))

    if property_schema.member_type in COMPARABLE_TYPES:
        if member_value < property_schema.member_min:
            value_errors.append(
                'The value of "%s" for "%s" fails min size of %s.' %
                (member_value, key, property_schema.member_min))


def validate_member_max(
        key: str,
        member_value: Any,
        property_schema: MetaSchemaType,
        value_errors: List[str]) -> None:
    """Validate a member of a collection for maximum allowable value.

    :param key: The name of the collection property to validate.
    :type key: str
    :param member_value: The member value of the collection property to
        validate.
    :type member_value: str, int, float, date, datetime, time
    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`property_type.PropertyType`
    :param value_errors: A list of errors found for a given value. If the
        validation fails, then an error message is added to the
        value_errors list.
    :type value_errors: list<str>
    :rtype: None
    """
    if property_schema.member_type is str:
        if len(member_value) > property_schema.member_max:
            value_errors.append(
                'The value of "%s" for "%s" fails max length of %s.' %
                (member_value, key, property_schema.member_max))

    if property_schema.member_type in COMPARABLE_TYPES:
        if member_value > property_schema.member_max:
            value_errors.append(
                'The value of "%s" for "%s" fails max size of %s.' %
                (member_value, key, property_schema.member_max))


def enum_validation(property_schema: MetaSchemaType, value: Any) -> bool:
    """Validate a non-collection property for value in an enumeration set.

    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`property_type.PropertyType`
    :param value: The value of the property to be validated.
    :type value: object
    :return: True if the validation is successful, else False.
    :rtype: bool
    """
    if property_schema.enum:
        if value not in property_schema.enum:
            return False
    return True


def min_validation(property_schema: MetaSchemaType, value: Any) -> bool:
    """Validate a non-collection property for minimum allowable value.

    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`property_type.PropertyType`
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


def max_validation(property_schema: MetaSchemaType, value: Any) -> bool:
    """Validates a non-collection property for maximum allowable value.

    :param property_schema: The property schema to utilize for validation.
    :type property_schema: :class:`property_type.PropertyType`
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


def non_none_singular_validation(
        key: str,
        property_schema: MetaSchemaType,
        value: Any,
        value_errors: List[str]) -> None:
    """Method to validate an object value meets schema requirements.

    This method validates non-collection properties. The method should
    only be used for non-None values.

    :param key: The name of the property that is being validated.
    :type key: str
    :param property_schema: The schema definition for the target property.
    :type property_schema: :class:`property_type.PropertyType`
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
                            (value, key,
                             _generate_sorted_list(property_schema.enum)))

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
        if property_schema.type is str and value is not '':
            if not re.match(property_schema.regex, value):
                value_errors.append(
                    'Value "%s" for %s does not meet regex: %s' %
                    (value, key, property_schema.regex))


SortableCollection = TypeVar(
    'SortableCollection', List[Any], Set[Any], Tuple[Any])


def _generate_sorted_list(some_collection: SortableCollection) -> List[Any]:
    """Attempt to generate a sorted list from a collection.

    :param some_collection: A collection that will attempt to be sorted.
    :return: The sorted collection if possible, else return original collection.
    """
    try:
        return sorted(some_collection)
    except TypeError:
        return list(some_collection)
