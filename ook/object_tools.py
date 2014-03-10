import re

from object_type import BaseType, PropertySchema, SchemaType

#: The `type_map` converts the string declaration of attribute type.
type_map = BaseType({
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'list': list,
    'set': set,
    'str': basestring,
})

collection_type_set = {dict, list, set}


def create_ook_type(name, schema):
    """

    :param name: The name to apply to the created class, with object_type.BaseType as parent.
    :type name: str
    :param schema: A representation of the schema in dictionary format.
    :type schema: dict
    :return: A class whose base is object_type.BaseType.
    :rtype: ClassType
    """
    if name is None or name is '':
        raise ValueError('The string "name" argument is required.')
    if schema is None:
        raise ValueError('The schema dictionary is required.')
    if not isinstance(schema, dict):
        raise ValueError('The schema must be a dict.')

    ook_type = type(name, (BaseType, ), dict())

    #todo: raul - add the actual validation of the schema
    finalized_schema = SchemaType()

    for key, value in schema.iteritems():
        finalized_schema[key] = PropertySchema(value)

    validate_schema(finalized_schema)

    ook_type._OOK_SCHEMA = finalized_schema

    validate_object(finalized_schema)

    return ook_type


def validate_schema(the_schema):
    """

    :param the_schema:
    :type the_schema: dict|ook.object_type.SchemaType
    :return:
    :rtype:
    """
    if not isinstance(the_schema, SchemaType):
        if isinstance(the_schema, dict) or isinstance(the_schema, BaseType):
            the_schema = SchemaType(the_schema)
        else:
            raise ValueError('"the_schema" argument must be of type dict, BaseType, or SchemaType')

    validate_object(the_schema)


def validate_object(the_object):
    """Method that will validate if an object meets the schema requirements.

    :param the_object: An object instance whose type is a child class of
        `ook.object.BaseType`
    :type the_object: ook.object_type.BaseType
    :except: ValueError - Thrown due to validation failures.
    """

    if not isinstance(the_object, BaseType):
        raise ValueError('Validation can only support validation of objects '
                         'derived from ook.BaseType')

    value_errors = []

    for key, metadata in the_object.get_schema().iteritems():
        required = metadata.get('required', False)
        value = the_object.get(key, None)
        value_type = type_map.get(metadata.get('type', None), None)
        item_type = type_map.get(metadata.get('item_type', None), None)

        # required: True | False
        if required and value is None:
            value_errors.append('The value for "%s" is required.' % key)

        # check for enumeration on non collection types
        if hasattr(metadata, 'enum'):
            if required or (not required and value is not None):
                if not value in metadata.enum:
                    value_errors.append(
                        'The value "%s" for "%s" must be in enumeration "%s".' %
                        (value, key, metadata.enum))

        # check if there is a value_type to continue processing
        if value_type and value is not None:
            # type checking
            if not isinstance(value, value_type):
                value_errors.append(
                    'The value for "%s" is not of type "%s": %s' %
                    (key, metadata.type, str(value)))
                continue  # don't assume successful testing based on value_type

            #todo: raul - split this up into collection and single validation.
            validate_value(key, metadata, value_type, value, value_errors)

    if value_errors:
        raise ValueError(str.join(' \n-- ', value_errors))


def validate_value(key, metadata, value_type, value, value_errors):
    """ Method to validate an object value meets schema requirements.
    :param key:
    :type key:
    :param metadata:
    :type metadata:
    :param value_type:
    :type value_type:
    :param value:
    :type value:
    :param value_errors:
    :type value_errors:
    :return:
    :rtype:
    """
    # min
    if hasattr(metadata, 'min'):
        if ((value_type is basestring or value_type in collection_type_set)
            and len(value) < metadata.min):
            value_errors.append(
                'The value for "%s" fails the minimum length of %s' %
                (key, metadata.min))
        elif (value_type is int or value_type is float) and value < metadata.min:
            value_errors.append(
                'The value of "%s" for "%s" is less than %s min.' %
                (value, key, metadata.min))

    # max
    if hasattr(metadata, 'max'):
        if ((value_type is basestring or value_type in collection_type_set)
            and len(value) > metadata.max):
            value_errors.append(
                'The value for "%s" fails the maximum length of %s' %
                (key, metadata.max))
        elif (value_type is int or value_type is float) and value > metadata.max:
            value_errors.append(
                'The value of "%s" for "%s" is more than "%s" max.' %
                (value, key, metadata.max))

    # regex validation
    if hasattr(metadata, 'regex'):
        if value_type is basestring and value is not '':
            if not re.match(metadata.regex, value):
                value_errors.append(
                    'Value for %s does not meet regex: %s' %
                    (key, metadata.regex))
        if value_type in {list, set}:
            for item_value in value:
                if not re.match(metadata.regex, item_value):
                    value_errors.append(
                        'Value %s in %s does not meet regex: %s' %
                        (item_value, key, metadata))

