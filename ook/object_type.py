"""The fundamental *Ook* base data types for creation of derived child classes.

Usage
------

The **object_type** module allows for the construction of **Ook** data types. A complete
configured data type definition would be constructed as::


    class MyType(BaseType):
        _OOK_SCHEMA = SchemaType({
            'some_property': PropertyType({
                'type': 'int',
                'required': True,
            }),
            'other_property': PropertyType({
                'type': 'str',
                'required': False,
                'enum': {'Enum1', 'Enum2', 'Enum3'}
            }),
        })

    my_object = MyType()
    my_object.some_property = 7
    # or
    my_object['some_property'] = 7

Classes
--------

"""


# The `type_map` converts the string declaration of attribute type.
TypeMap = {
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'list': list,
    'set': set,
    'str': basestring,
}

# The `collection_type_set` is the set of supported collection types.
CollectionTypeSet = {dict, list, set}


class _CoreType(dict):
    """The root type of *Ook* types.

    **_CoreType** ensures that *Ook* objects can be access by either dict key or object attribute.

    :Example:
    >>> some_object = _CoreType({'key1': 'value1'})
    >>> assert some_object.key1 == 'value1'
    >>> assert some_object['key1'] == 'value1'
    >>> some_object.key2 = 'value2'
    >>> assert some_object['key2'] == 'value2'
    >>> some_object['key3'] = 'value3'
    >>> assert some_object.key3 == 'value3'
    """

    def __init__(self, *args, **kwargs):
        """**_CoreType** initialized as a `dict` type.

        :param args: Args to be passed to `dict` parent class.
        :type args: list
        :param kwargs: Named args to be passed to `dict` parent class.
        :type kwargs: dict

        Initializes the accessor behavior to allow for property access as dict key or object
        attribute.
        """
        # noinspection PyTypeChecker
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self


class SchemaType(_CoreType):
    """The type definition for a schema object.

    The **SchemaType** contains a dictionary of property field names and the corresponding
    **PropertySchema** definition.

    Example SchemaType representation::

        SchemaType({
          'some_property': PropertySchema({
                'type': 'str',
                'required': True
            })
        })
    """
    pass


class BaseType(_CoreType):
    """BaseType provides the **Ook** schema interface.

    The **BaseType** provides the schema management functionality to a derived **Ook** type
    instance.
    """

    #: The Ook schema pointer.
    _OOK_SCHEMA = SchemaType()

    @classmethod
    def get_schema(cls):
        """Returns the **SchemaType** instance for a given **Ook** type.

        :return: The schema metadata definition for the BaseType derived
            child type.
        :rtype: ook.object_type.SchemaType.
        """
        return cls._OOK_SCHEMA


class PropertySchema(BaseType):
    """The object type for representing Property schema definitions.

    *Property Schema Settings*:

        *type*
            datetime*, date*, time*, str, int, float, bool, dict, set, list, none. Defaults to
            None.
        *required*
            True|False. Defaults False.
        *min*
            float. Defaults to None.
        *max*
            float. Defaults to None.
        *regex*
            string. Defaults to None.
        *item_type*
            datetime*, date*, time*, str, int, float, bool, dict, set, list, none. Default to None.
        *tem_min*
            float. Defaults to None.
        *item_max*
            float, Defaults to None.

    \* - Are to be added in subsequent versions.
    """
    #: todo: Add support for datetime, date & time
    _OOK_SCHEMA = BaseType({
        'type': BaseType({
            'type': 'str',
            'required': False,
            'enum': {'bool', 'dict', 'float', 'int', 'list', 'set', 'str'}
        }),
        'required': BaseType({
            'type': 'bool',
            'required': False,
        }),
        'enum': BaseType({
            'type': 'set',
            'required': False,
        }),
        'min': BaseType({
            'type': float,
            'required': False,
        }),
        'max': BaseType({
            'type': float,
            'required': False,
        }),
        'regex': BaseType({
            'type': 'str',
            'required': False,
            'min': 1,
        }),
        'item_type': {
            'type': 'str',
            'required': False,
            'enum': {'bool', 'dict', 'float', 'int', 'list', 'set', 'str'}
        },
        'item_min': BaseType({
            'type': float,
            'required': False,
        }),
        'item_max': BaseType({
            'type': float,
            'required': False,
        }),
    })

