class _CoreType(dict):
    def __init__(self, *args, **kwargs):
        # noinspection PyTypeChecker
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self


class BaseType(_CoreType):
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
    """
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
    })


class SchemaType(BaseType):
    pass

