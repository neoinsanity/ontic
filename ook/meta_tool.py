import re

from meta_type import CollectionTypeSet, TypeMap

_COMPARABLE_TYPES = {'int', 'float', 'date', 'time', 'datetime'}


def validate_value(name, property_schema, value, value_errors):
    """Method to validate a given value against a given property schema.

    :param name: The name of the value to be validated.
    :type name: str
    :param property_schema: The property schema that contains the validation rules.
    :type property_schema: ook.schema_type.SchemaProperty
    :param value: The value that is to be validated.
    :type value: object
    :param value_errors: A list that is utilized to collect the errors found during schema
        validation.
    :type value_errors: list
    """
    # required: True | False
    if property_schema.required and value is None:
        value_errors.append('The value for "%s" is required.' % name)
        return  # No other validation can occur without the required value

    if value is not None:
        validate_non_none_value(name, property_schema, value, value_errors)


def validate_non_none_value(key, property_schema, value, value_errors):
    """

    :param key:
    :type key:
    :param property_schema:
    :type property_schema:
    :param value:
    :type value:
    :param value_errors:
    :type value_errors:
    :return:
    :rtype:
    """
    # Divide between single and collection types for validation processing.
    schema_value_type = TypeMap.get(property_schema.get('type', None), None)

    if not schema_value_type:
        # if no schema_type, then just check that the value is in an enum if
        # necessary.
        if not enum_validation(property_schema, value):
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

        if schema_value_type in CollectionTypeSet:
            validate_collections(key, property_schema, value, value_errors)
        else:
            if not enum_validation(property_schema, value):
                value_errors.append(
                    'The value "%s" for "%s" not in enumeration %s.' %
                    (value, key, list(property_schema.enum)))
                return  # No further processing can occur

            #todo: raul - split this up into collection and single validation.
            non_none_value_validation(key, property_schema, value, value_errors)


def validate_collections(key, property_schema, value, value_errors):
    """

    :param key:
    :type key:
    :param property_schema:
    :type property_schema:
    :param value:
    :type value:
    :param value_errors:
    :type value_errors:
    :return:
    :rtype:
    """
    if not min_validation(property_schema, value):
        value_errors.append('The value of "%s" for "%s" fails min of %s.' %
                            (value, key, property_schema.min))

    if not max_validation(property_schema, value):
        value_errors.append('The value of "%s" for "%s" fails max of %s.' %
                            (value, key, property_schema.max))

    if property_schema.type in {'list', 'set'}:
        validation_list = list()
        if property_schema.enum:
            def validate_enum(item, property_schema, value_errors):
                if not enum_validation(property_schema, item):
                    value_errors.append(
                        'The value "%s" for "%s" not in enumeration %s.' %
                        (item, value, list(property_schema.enum)))

            validation_list.append(validate_enum)

        if property_schema.item_type:
            def validate_item_type(item, property_schema, value_errors):
                schema_value_type = TypeMap.get(property_schema.item_type)
                if not isinstance(item, schema_value_type):
                    value_errors.append(
                        'The value for "%s" is not of type "%s": %s' %
                        (value, property_schema.item_type, str(item)))

            validation_list.append(validate_item_type)

            if property_schema.regex and property_schema.item_type == 'str':
                def validate_item_regex(item, property_schema, value_errors):
                    if not re.match(property_schema.regex, item):
                        value_errors.append(
                            'Value "%s" for %s does not meet regex: %s' %
                            (item, value, property_schema.regex))

                validation_list.append(validate_item_regex)

        if property_schema.item_min:
            def validate_item_min(item, property_schema, value_errors):
                if ((property_schema.item_type == 'str') and
                            len(item) < property_schema.item_min):
                    value_errors.append(
                        'The value of "%s" for "%s" fails min of %s.' %
                        (item, value, property_schema.item_min))
                elif ((property_schema.item_type in _COMPARABLE_TYPES)
                      and item < property_schema.item_min):
                    value_errors.append(
                        'The value of "%s" for "%s" fails min of %s.' %
                        (item, value, property_schema.item_min))

            validation_list.append(validate_item_min)

        if property_schema.item_max:
            def validate_item_max(item, property_schema, value_errors):
                if ((property_schema.item_type == 'str') and
                            len(item) > property_schema.item_max):
                    value_errors.append(
                        'The value of "%s" for "%s" fails max of %s.' %
                        (item, value, property_schema.item_max))
                elif ((property_schema.item_type in _COMPARABLE_TYPES)
                      and item > property_schema.item_max):
                    value_errors.append(
                        'The value of "%s" for "%s" fails max of %s.' %
                        (item, value, property_schema.item_max))

            validation_list.append(validate_item_max)

        for item_value in value:
            validate_collection_item_value(item_value,
                                           property_schema,
                                           validation_list,
                                           value_errors)


def validate_collection_item_value(
        item, property_schema, validation_list, value_errors):
    """

    :param item:
    :type item: bool, list, set, int, str, float,
    :param property_schema:
    :type property_schema:
    :param validation_list:
    :type validation_list: list
    :param value_errors:
    :type value_errors: list
    :return:
    :rtype:
    """
    for validation in validation_list:
        validation(item, property_schema, value_errors)


def enum_validation(property_schema, value):
    if property_schema.enum:
        if not value in property_schema.enum:
            return False
    return True


def min_validation(property_schema, value):
    if property_schema.min:
        if ((property_schema.type == 'str' or
                     property_schema.type in {'list', 'set', 'dict'})
            and len(value) < property_schema.min):
            return False
        elif (property_schema.type in _COMPARABLE_TYPES and
                      value < property_schema.min):
            return False

    return True


def max_validation(property_schema, value):
    if property_schema.max:
        if ((property_schema.type == 'str' or
                     property_schema.type in {'list', 'set', 'dict'})
            and len(value) > property_schema.max):
            return False
        elif (property_schema.type in _COMPARABLE_TYPES and
                      value > property_schema.max):
            return False

    return True


def non_none_value_validation(key, property_schema, value, value_errors):
    """ Method to validate an object value meets schema requirements.

    :param key:
    :type key:
    :param property_schema:
    :type property_schema:
    :param value:
    :type value:
    :param value_errors:
    :type value_errors:
    :return:
    :rtype:
    """
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
        if property_schema.type == 'str' and value is not '':
            if not re.match(property_schema.regex, value):
                value_errors.append(
                    'Value "%s" for %s does not meet regex: %s' %
                    (value, key, property_schema.regex))
