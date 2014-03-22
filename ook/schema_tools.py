import re

from schema_type import CollectionTypeSet, SchemaType, SchemaProperty, TypeMap


def perfect_schema(candidate_schema):
    if candidate_schema is None:
        raise ValueError('candidate_schema must be provided.')
    if not isinstance(candidate_schema, SchemaType):
        raise ValueError('candidate_schema must be of SchemaType.')

    for property_schema in candidate_schema.values():
        perfect_schema_property(property_schema)


def validate_schema(candidate_schema):
    """

    :param candidate_schema:
    :type candidate_schema:
    :return:
    :rtype:
    """
    if candidate_schema is None:
        raise ValueError('candidate_schema must be provided.')
    if not isinstance(candidate_schema, SchemaType):
        raise ValueError('candidate_schema must be of SchemaType.')


def perfect_schema_property(candidate_schema_property):
    if candidate_schema_property is None:
        raise ValueError('candidate_schema_property must be provided.')
    if not isinstance(candidate_schema_property, SchemaProperty):
        raise ValueError('candidate_schema_property must be SchemaProperty type.')

    schema_property_schema = candidate_schema_property.get_schema()

    extra_properties = set(candidate_schema_property.keys()) - set(schema_property_schema.keys())
    for property_name in extra_properties:
        del candidate_schema_property[property_name]

    for property_name, property_schema in schema_property_schema.iteritems():
        if property_name not in candidate_schema_property:
            if property_schema.required:
                candidate_schema_property[property_name] = property_schema.default


def validate_schema_property(candidate_schema_property):
    """

    :param candidate_schema_property:
    :type candidate_schema_property:
    :return:
    :rtype:
    """
    if candidate_schema_property is None:
        raise ValueError('candidate_schema_property must be provided.')
    if not isinstance(candidate_schema_property, SchemaProperty):
        raise ValueError('candidate_schema_property must be SchemaProperty type.')

    value_errors = []

    for schema_setting, setting_schema in candidate_schema_property.get_schema().iteritems():
        setting_value = candidate_schema_property.get(schema_setting, None)

        _validate_value(schema_setting, setting_schema, setting_value, value_errors)


def _validate_value(key, property_schema, value, value_errors):
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

    # required: True | False
    if property_schema.required and value is None:
        value_errors.append('The value for "%s" is required.' % key)
        return  # No other validation can occur without the required value

    if value is not None:
        _validate_non_none_value(key, property_schema, value, value_errors)


def _validate_non_none_value(key, property_schema, value, value_errors):
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
        # if no schema_type, then just check that the value is in an enum if necessary.
        if not _enum_validation(property_schema, value):
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
            return  # If not of the expected type, than can't further validate without errors.

        if schema_value_type in CollectionTypeSet:
            _validate_collections(key, property_schema, value, value_errors)
        else:
            if not _enum_validation(property_schema, value):
                value_errors.append(
                    'The value "%s" for "%s" not in enumeration %s.' %
                    (value, key, list(property_schema.enum)))
                return  # No further processing can occur

            #todo: raul - split this up into collection and single validation.
            _non_none_value_validation(key, property_schema, value, value_errors)


def _validate_collections(key, property_schema, value, value_errors):
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
    if not _min_validation(property_schema, value):
        value_errors.append('The value of "%s" for "%s" fails min of %s.' %
                            (value, key, property_schema.min))

    if not _max_validation(property_schema, value):
        value_errors.append('The value of "%s" for "%s" fails max of %s.' %
                            (value, key, property_schema.max))

    if property_schema.type in {'list', 'set'}:
        validation_list = list()
        if property_schema.enum:
            def validate_enum(item, property_schema, value_errors):
                if not _enum_validation(property_schema, item):
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

            if property_schema.regex and property_schema.type == 'str':
                def validate_item_regex(item, property_schema, value_errors):
                    if not re.match(property_schema.regex, value):
                        value_errors.append(
                            'Value "%s" for %s does not meet regex: %s' %
                            (item, value, property_schema.regex))

                validation_list.append(validate_item_regex)

        if property_schema.item_min:
            def validate_item_min(item, property_schema, value_errors):
                if ((property_schema.item_type == 'str') and
                            len(item) < property_schema.item_min):
                    value_errors.append('The value of "%s" for "%s" fails min of %s.' %
                                        (item, value, property_schema.type_min))
                elif ((property_schema.item_type in {'int', 'float'})
                      and item < property_schema.type_min):
                    value_errors.append('The value of "%s" for "%s" fails min of %s.' %
                                        (item, value, property_schema.min))

            validation_list.append(validate_item_min)

        if property_schema.item_max:
            def validate_item_max(item, property_schema, value_errors):
                if ((property_schema.item_type == 'str') and
                            len(item) > property_schema.item_max):
                    value_errors.append('The value of "%s" for "%s" fails max of %s.' %
                                        (item, value, property_schema.type_min))
                elif ((property_schema.item_type in {'int', 'float'})
                      and item < property_schema.type_max):
                    value_errors.append('The value of "%s" for "%s" fails max of %s.' %
                                        (item, value, property_schema.max))

            validation_list.append(validate_item_max)

        for item_value in value:
            _validate_collection_item_value(item_value,
                                            property_schema,
                                            validation_list,
                                            value_errors)


def _validate_collection_item_value(item, property_schema, validation_list, value_errors):
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


def _enum_validation(property_schema, value):
    if property_schema.enum:
        if not value in property_schema.enum:
            return False
    return True


def _min_validation(property_schema, value):
    if property_schema.min:
        if ((property_schema.type == 'str' or
                     property_schema.type in {'list', 'set', 'dict'})
            and len(value) < property_schema.min):
            return False
        elif ((property_schema.type == 'int' or property_schema.type == 'float')
              and value < property_schema.min):
            return False

    return True


def _max_validation(property_schema, value):
    if property_schema.max:
        if ((property_schema.type == 'str' or
                     property_schema.type in {'list', 'set', 'dict'})
            and len(value) > property_schema.max):
            return False
        elif ((property_schema.type == 'int' or property_schema.type == 'float')
              and value > property_schema.max):
            return False

    return True


def _non_none_value_validation(key, property_schema, value, value_errors):
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
    if not _min_validation(property_schema, value):
        value_errors.append('The value of "%s" for "%s" fails min of %s.' %
                            (value, key, property_schema.min))

    # max
    if not _max_validation(property_schema, value):
        value_errors.append('The value of "%s" for "%s" fails max of %s.' %
                            (value, key, property_schema.max))

    # regex validation
    if property_schema.regex:
        if property_schema.type == 'str' and value is not '':
            if not re.match(property_schema.regex, value):
                value_errors.append(
                    'Value "%s" for %s does not meet regex: %s' %
                    (value, key, property_schema.regex))
