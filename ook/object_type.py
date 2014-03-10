"""The fundamental *Ook* base data types for creation of derived child classes.

"""


class _CoreType(dict):
    """The root type of *Ook* types.

    *_CoreType* ensures that *Ook* objects can be access by either dict key or object attribute.

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
        """*CoreType* initialized as a `dict` type.

        :param args: Args to be passed to `dict` parent class.
        :type args: list
        :param kwargs: Named args to be passed to `dict` parent class.
        :type kwargs: dict
        """
        # noinspection PyTypeChecker
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self


class BaseType(_CoreType):
    """The base type of a *Ook*"""
    _OOK_SCHEMA = dict()

    @classmethod
    def get_schema(cls):
        """

        :return: The schema metadata definition for the BaseType derived
            child type.
        :rtype: ook.object_type.BaseType.
        """
        return cls._OOK_SCHEMA


class PropertySchema(BaseType):
    """The object type for representing Property schema definitions.

    **Property Schema Settings**::

        {
            type: datetime, date, time, str, int, float, bool, dict, set, list,
                none. Defaults to None
            required: True| False, defaults False.
            min: int
            max: int
            regex: string
            item_type: datetime, date, time, str, int, float, bool, dict,
                set, list, none
            item_min: int,
            item_max: int,
        }
    """
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
        })
    })


class SchemaType(BaseType):
    pass

