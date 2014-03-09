class _CoreType(dict):
    def __init__(self, *args, **kwargs):
        # noinspection PyTypeChecker
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self


class PropertySchema(_CoreType):
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
    _OOK_SCHEMA = _CoreType({
        'type': _CoreType({
            'type': 'str',
            'required': False,
        }),
        'required': _CoreType({
            'type': 'bool',
            'required': False
        }),
    })


class SchemaType(_CoreType):
    pass


class BaseType(_CoreType):
    _OOK_SCHEMA = SchemaType()

    @classmethod
    def get_schema(cls):
        """

        :return: The schema metadata definition for the BaseType derived
            child type.
        :rtype: ook.object_type.BaseType.
        """
        return cls._OOK_SCHEMA
