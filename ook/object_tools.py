"""The **object_tools** provides the methods to create and validate **Ook** types and objects.

Usage
======

There are two basic operations provided by **object_tools**; schema definition and object
handling. Schema definition entails type creation and validation.

Schema Tools
-------------

To validate a schema definition, utilize the :meth:`~ook.object_tools.validate_schema` method.

Schema are composed of :class:`~ook.object_type.PropertySchema` objects. If there is a need,
individual **PropertySchema** objects can be validated individually with the
:meth:`~ook.object_tools.validate_property` method.

To create a python type for a given :class:`~ook.object_type.SchemaType` utilize the
:meth:`~ook.object_tools.create_ook_type` method. **Ook** object instances created by a generated
type are child classes of the :class:`~ook.object_types` class.

Object Tools
-------------

**Ook** objects created by either subclassing :class:`~ook.object_type.BaseType` or via
:meth:`~create_ook_type`, will need to be validated. Utilize the
**Ook** object :meth:`~ook.object_tools.validate_object` method for validation.

If the need should arise for validation of an **Ook** object by value, utilize the
:meth:`~ook.object_tools.validate_value` method.

"""
import re

from object_type import BaseType, CollectionTypeSet, PropertySchema, SchemaType, TypeMap


def create_ook_type(name, schema):
    """Create an **Ook** type to generate objects with a given schema.

    :param name: The name to apply to the created class, with object_type.BaseType as parent.
    :type name: str
    :param schema: A representation of the schema in dictionary format.
    :type schema: dict
    :return: A class whose base is object_type.BaseType.
    :rtype: ClassType
    :except ValueError: String name required. Dict or SchemaType schema required.
    """
    if name is None or name is '':
        raise ValueError('The string "name" argument is required.')
    if schema is None:
        raise ValueError('The schema dictionary is required.')
    if not isinstance(schema, dict):
        raise ValueError('The schema must be a dict or SchemaType.')

    ook_type = type(name, (BaseType, ), dict())

    finalized_schema = SchemaType()

    for property_name, property_schema_candidate in schema.iteritems():
        finalized_schema[property_name] = _confirm_property_schema(property_schema_candidate)

    ook_type._OOK_SCHEMA = finalized_schema

    return ook_type


def validate_object(the_object):
    """Method that will validate if an object meets the schema requirements.

    :param the_object: An object instance whose type is a child class of
        :class:`~ook.object_type.BaseType`
    :type the_object: ook.object_type.BaseType
    :except ValueError:
        * *the_object* is not a :class:`~ook.object_type.BaseType`.

        * A property of *the_object* does not meet schema requirements.

    """

    if not isinstance(the_object, BaseType):
        raise ValueError(
            'Validation can only support validation of objects derived from ook.BaseType.')

    value_errors = []

    for property_name, property_schema in the_object.get_schema().iteritems():
        value = the_object.get(property_name, None)

        _validate_value(property_name, property_schema, value, value_errors)

    if value_errors:
        raise ValueError(str.join(' \n', value_errors))


def validate_property_schema(the_property):
    """Method to validate if a schema property object is a valid definition.

    :param the_property: The object to be validated as a :class:`~ook.object_type.PropertySchema`
        candidate.
    :type ook.object_type.PropertySchema|dict:
    :except ValueError: *the_property* is  not dict, :class:`~ook.object_type.BaseType`
        or :class:`~.ook.object_type.PropertySchema`.
    """
    if not isinstance(the_property, dict):
        raise ValueError(
            '"the_property" argument must be of type dict, BaseType, or PropertySchema.')

    _confirm_property_schema(the_property)


def validate_schema(property_schema):
    """Determine if a schema definition is a valid :class:`~ook.object_type.SchemaType` candidate.

    :param property_schema: The schema definition candidate.
    :type property_schema: dict|ook.object_type.SchemaType
    :except ValueError:

        * *property_schema* is not a dict, **BaseType**, or *SchemaType*.

        * *property_schema* is not a valid **Ook** schema definition.
    """
    if not isinstance(property_schema, dict):
        raise ValueError(
            '"property_schema" argument must be of type dict, BaseType, or SchemaType,')

    _generate_schema_from_dict(property_schema)


def validate_value(value, property_schema):
    """Validate a value against a given **PropertySchema**

    :param value: The value to be validated against the given **PropertySchema**.
    :type value: object
    :param property_schema: The **PropertySchema** utilized for validation.
    :type property_schema:  dict, ook.object_tools.BaseType, ook.object_tools.PropertySchema
    :except ValueError:

        - Responds with a value error if the validation is not successful.

        - "property_schema" is not provided or not a dict, **BaseType**, or **PropertySchema**
    """
    if property_schema is None:
        raise ValueError('"property_schema" is not provided.')
    if not isinstance(property_schema, dict):
        raise ValueError('"property_schema" is not of type dict, BaseType, or PropertySchema.')

    if not isinstance(property_schema, PropertySchema):
        property_schema = _confirm_property_schema(property_schema)

    value_errors = []

    _validate_value('value', property_schema, value, value_errors)

    if value_errors:
        raise ValueError(str.join(' \n', value_errors))


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
    required = property_schema.get('required', False)
    if required and value is None:
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
        if schema_value_type in CollectionTypeSet:
            _validate_collections(key, property_schema, value, value_errors)
        else:
            # type checking
            if not isinstance(value, schema_value_type):
                value_errors.append(
                    'The value for "%s" is not of type "%s": %s' %
                    (key, property_schema.type, str(value)))
                return  # If not of the expected type, than can't further validate without errors.

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
        return

    if not _max_validation(property_schema, value):
        value_errors.append('The value of "%s" for "%s" fails max of %s.' %
                            (value, key, property_schema.max))


def _enum_validation(property_schema, value):
    if property_schema.get('enum', None):
        if not value in property_schema.enum:
            return False
    return True


def _min_validation(property_schema, value):
    if hasattr(property_schema, 'min'):
        if ((property_schema.type == 'str' or
                     property_schema.type in {'list', 'set', 'dict'})
            and len(value) < property_schema.min):
            return False
        elif ((property_schema.type == 'int' or property_schema.type == 'float')
              and value < property_schema.min):
            return False

    return True


def _max_validation(property_schema, value):
    if hasattr(property_schema, 'max'):
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
    if hasattr(property_schema, 'regex'):
        if property_schema.type == 'str' and value is not '':
            if not re.match(property_schema.regex, value):
                value_errors.append(
                    'Value "%s" for %s does not meet regex: %s' %
                    (value, key, property_schema.regex))
        if property_schema.type in {'list', 'set'}:
            for item_value in value:
                if not re.match(property_schema.regex, item_value):
                    value_errors.append(
                        'Value %s in %s does not meet regex: %s' %
                        (item_value, key, property_schema))


def _generate_schema_from_dict(schema_dict):
    """Generates a PropertySchema from a dict."""
    schema_object = PropertySchema(schema_dict)
    for key, property_schema in schema_dict.iteritems():
        schema_object['key'] = _confirm_property_schema(property_schema)

    return schema_dict


def _confirm_property_schema(property_schema_candidate):
    """

    :param property_schema_candidate:
    :type property_schema_candidate:
    :return:
    :rtype:
    """
    if not isinstance(property_schema_candidate, PropertySchema):
        property_schema_candidate = PropertySchema(property_schema_candidate)

    validate_object(property_schema_candidate)

    return property_schema_candidate
