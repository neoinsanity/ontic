import meta_tools
from schema_type import SchemaType, SchemaProperty


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
        raise ValueError('"candidate_schema" must be provided.')
    if not isinstance(candidate_schema, SchemaType):
        raise ValueError('"candidate_schema" must be of SchemaType.')

    value_errors = []
    for candidate_property_schema in candidate_schema.values():
        validate_schema_property(candidate_property_schema)

    return value_errors


def perfect_schema_property(candidate_schema_property):
    if candidate_schema_property is None:
        raise ValueError('candidate_schema_property must be provided.')
    if not isinstance(candidate_schema_property, SchemaProperty):
        raise ValueError(
            'candidate_schema_property must be SchemaProperty type.')

    schema_property_schema = candidate_schema_property.get_schema()

    extra_properties = set(candidate_schema_property.keys()) - set(
        schema_property_schema.keys())
    for property_name in extra_properties:
        del candidate_schema_property[property_name]

    for property_name, property_schema in schema_property_schema.iteritems():
        if property_name not in candidate_schema_property:
            if property_schema.required:
                candidate_schema_property[
                    property_name] = property_schema.default


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
        raise ValueError(
            'candidate_schema_property must be SchemaProperty type.')

    value_errors = []

    for schema_setting, setting_schema in candidate_schema_property \
            .get_schema().iteritems():
        setting_value = candidate_schema_property.get(schema_setting, None)

        meta_tools._validate_value(schema_setting,
                                   setting_schema,
                                   setting_value,
                                   value_errors)



