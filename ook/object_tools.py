"""The **object_tools** provides the methods to create and validate **Ook**
types and objects.

Usage
======

There are two basic operations provided by **object_tools**; schema
definition and object handling. Schema definition entails type creation and
validation.

Schema Tools
-------------

To validate a schema definition, utilize the
:meth:`~ook.object_tools.validate_schema` method.

Schema are composed of :class:`~ook.object_type.PropertySchema` objects. If
there is a need, individual **PropertySchema** objects can be validated
individually with the :meth:`~ook.object_tools.validate_property` method.

To create a python type for a given :class:`~ook.object_type.SchemaType`
utilize the :meth:`~ook.object_tools.create_ook_type` method. **Ook** object
instances  created by a generated type are child classes of the
:class:`~ook.object_types` class.

Object Tools
-------------

**Ook** objects created by either subclassing
:class:`~ook.object_type.BaseType` or via :meth:`~create_ook_type`, will need
to be validated. Utilize the **Ook** object
:meth:`~ook.object_tools.validate_object` method for validation.

If the need should arise for validation of an **Ook** object by value,
utilize the :meth:`~ook.object_tools.validate_value` method.
"""
import re

from object_type import BaseType, PropertySchema, SchemaType

# : The `type_map` converts the string declaration of attribute type.
type_map = {'bool': bool, 'dict': dict, 'float': float, 'int': int,
            'list': list, 'set': set, 'str': basestring, }

# : The `collection_type_set` is the set of supported collection types.
collection_type_set = {dict, list, set}


def create_ook_type(name, schema):
    """Create an **Ook** type to generate objects with a given schema.

    :param name: The name to apply to the created class,
        with object_type.BaseType as parent.
    :type name: str
    :param schema: A representation of the schema in dictionary format.
    :type schema: dict
    :return: A class whose base is object_type.BaseType.
    :rtype: ClassType
    :except ValueError: String name required. Dict or SchemaType schema
        required.
    """
    if name is None or name is '':
        raise ValueError('The string "name" argument is required.')
    if schema is None:
        raise ValueError('The schema dictionary is required.')
    if not isinstance(schema, dict):
        raise ValueError('The schema must be a dict or SchemaType.')

    ook_type = type(name, (BaseType, ), dict())

    finalized_schema = SchemaType()

    for key, value in schema.iteritems():
        property_schema = PropertySchema(value)
        validate_object(property_schema)
        finalized_schema[key] = property_schema

    ook_type.OOK_SCHEMA = finalized_schema

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
            'Validation can only support validation of objects derived from '
            'ook.BaseType.')

    value_errors = []

    for key, metadata in the_object.get_schema().iteritems():
        required = metadata.get('required', False)
        value = the_object.get(key, None)
        value_type = type_map.get(metadata.get('type', None), None)

        # required: True | False
        if required and value is None:
            value_errors.append('The value for "%s" is required.' % key)

        # check for enumeration on non collection types
        if hasattr(metadata, 'enum'):
            if required or (not required and value is not None):
                if not value in metadata.enum:
                    value_errors.append(
                        'The value "%s" for "%s" not in enumeration %s.' % (
                            value, key, list(metadata.enum)))

        # check if there is a value_type to continue processing
        if value_type and value is not None:
            # type checking
            if not isinstance(value, value_type):
                value_errors.append(
                    'The value for "%s" is not of type "%s": %s' % (
                        key, metadata.type, str(value)))
                continue  # don't assume successful testing based on value_type

            # todo: raul - split this up into collection and single validation.
            validate_value(key, metadata, value_type, value, value_errors)

    if value_errors:
        raise ValueError(str.join(' \n-- ', value_errors))


def validate_property(the_property):
    """Method to validate if a schema property object is a valid definition.

    :param the_property: The object to be validated as a
        :class:`~ook.object_type.PropertySchema` candidate.
    :type ook.object_type.PropertySchema|dict:
    :except ValueError: *the_property* is  not dict,
        :class:`~ook.object_type.BaseType` or
        :class:`~.ook.object_type.PropertySchema`.
    """
    if not isinstance(the_property, PropertySchema):
        if isinstance(the_property, dict) or isinstance(the_property, BaseType):
            the_property = PropertySchema(the_property)
        else:
            raise ValueError(
                '"the_property" argument must be of type dict, BaseType, '
                'or PropertySchema.')

    validate_object(the_property)


def validate_schema(the_schema):
    """Determine if a schema definition is a valid
    :class:`~ook.object_type.SchemaType` candidate.

    :param the_schema: The schema definition candidate.
    :type the_schema: dict|ook.object_type.SchemaType
    :except ValueError:

        * *the_schema* is not a dict, **BaseType**, or *SchemaType*.

        * *the_schema* is not a valid **Ook** schema definition.
    """
    if not isinstance(the_schema, SchemaType):
        if isinstance(the_schema, dict) or isinstance(the_schema, BaseType):
            the_schema = SchemaType(the_schema)
        else:
            raise ValueError(
                '"the_schema" argument must be of type dict, BaseType, '
                'or SchemaType,')

    # todo: raul - validation should happen like this, but will defer until
    # nested validation.
    # validate_object(the_schema)

    for the_property in the_schema.values():
        validate_property(the_property)


# todo: raulg - This is going to get revamped in next rev.
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
        if ((value_type is basestring or value_type in collection_type_set) and
                    len(value) < metadata.min):
            value_errors.append(
                'The value for "%s" fails the minimum length of %s' % (
                    key, metadata.min))
        elif ((value_type is int or value_type is float) and
                      value < metadata.min):
            value_errors.append(
                'The value of "%s" for "%s" is less than %s min.' % (
                    value, key, metadata.min))

    # max
    if hasattr(metadata, 'max'):
        if ((value_type is basestring or value_type in collection_type_set) and
                    len(value) > metadata.max):
            value_errors.append(
                'The value for "%s" fails the maximum length of %s' % (
                    key, metadata.max))
        elif ((value_type is int or value_type is float) and
                      value > metadata.max):
            value_errors.append(
                'The value of "%s" for "%s" is more than "%s" max.' % (
                    value, key, metadata.max))

    # regex validation
    if hasattr(metadata, 'regex'):
        if value_type is basestring and value is not '':
            if not re.match(metadata.regex, value):
                value_errors.append(
                    'Value "%s" for %s does not meet regex: %s' % (
                        value, key, metadata.regex))
        if value_type in {list, set}:
            for item_value in value:
                if not re.match(metadata.regex, item_value):
                    value_errors.append(
                        'Value %s in %s does not meet regex: %s' % (
                            item_value, key, metadata))

