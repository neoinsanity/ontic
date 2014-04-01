"""The base class for deriving types that require schema support.


.. image:: images/object_types.jpg

Usage
------

"""

from datetime import date, datetime, time
import re

#: The set of comparable types.
_COMPARABLE_TYPES = {'int', 'float', 'date', 'time', 'datetime'}

#: Used to convert the string declaration of attribute type to native type.
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

#: The set of supported collection types.
SUPPORTED_COLLECTION_TYPES = {dict, list, set}


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

        :param args: Args to be passed to `dict` parent class.
        :type args: list
        :param kwargs: Named args to be passed to `dict` parent class.
        :type kwargs: dict

        Initializes the accessor behavior to allow for property access as
        dict key or object
        attribute.
        """
        # noinspection PyTypeChecker
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self


class MetaType(CoreType):
    """

    """
    #: The Ook schema pointer.
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

    *Property Schema Settings*:

        *type*
            datetime, date, time, str, int, float, bool, dict, set, list, none.
            Defaults to None.
        *required*
            True|False. Defaults False.
        *min*
            float. Defaults to None.
        *max*
            float. Defaults to None.
        *regex*
            string. Defaults to None.
        *item_type*
            datetime*, date*, time*, str, int, float, bool, dict, set, list,
            none. Default to None.
        *tem_min*
            float. Defaults to None.
        *item_max*
            float, Defaults to None.

    """
    OOK_SCHEMA = CoreType({
        'type': MetaType({
            'type': 'str',
            'default': None,
            'required': True,
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
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'default': MetaType({
            'type': 'bool',
            'default': False,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'required': MetaType({
            'type': 'bool',
            'default': False,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'enum': MetaType({
            'type': 'set',
            'default': None,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'min': MetaType({
            'type': float,
            'default': None,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'max': MetaType({
            'type': float,
            'default': None,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'regex': MetaType({
            'type': 'str',
            'default': None,
            'required': True,
            'enum': None,
            'min': 1,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'item_type': MetaType({
            'type': 'str',
            'default': None,
            'required': True,
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
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'item_min': MetaType({
            'type': float,
            'default': None,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'item_max': MetaType({
            'type': float,
            'default': None,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
    })

    def __init__(self, *args, **kwargs):
        MetaType.__init__(self, *args, **kwargs)

        perfect_schema_property(self)
        validate_schema_property(self)


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
    schema_value_type = TYPE_MAP.get(property_schema.get('type', None), None)

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

        if schema_value_type in SUPPORTED_COLLECTION_TYPES:
            validate_collections(key, property_schema, value, value_errors)
        else:
            if not enum_validation(property_schema, value):
                value_errors.append(
                    'The value "%s" for "%s" not in enumeration %s.' %
                    (value, key, list(property_schema.enum)))
                return  # No further processing can occur

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
                schema_value_type = TYPE_MAP.get(property_schema.item_type)
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


def perfect_schema_property(candidate_schema_property):
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
        raise ValueError('"candidate_schema_property" must be provided.')
    if not isinstance(candidate_schema_property, SchemaProperty):
        raise ValueError(
            '"candidate_schema_property" must be SchemaProperty type.')

    value_errors = []

    for schema_setting, setting_schema in (
            candidate_schema_property.get_schema().iteritems()):
        setting_value = candidate_schema_property.get(schema_setting, None)

        validate_value(schema_setting,
                       setting_schema,
                       setting_value,
                       value_errors)
