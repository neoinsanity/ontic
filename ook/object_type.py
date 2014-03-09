
class BaseType(dict):

    _OOK_META = dict()

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    @classmethod
    def get_schema(cls):
        """

        :return: The schema metadata definition for the BaseType derived
            child type.
        :rtype: ook.object_type.BaseType.
        """
        return cls._OOK_SCHEMA


class OokMetaRecord(BaseType):
    """
    {
        type: datatime, date, time, str, int, float, bool, dict, set, list,
            none. Defaults to None
        required: True| False, defaults False.
        min: int
        max: int
        regex: string
        item_type: datatime, date, time, str, int, float, bool, dict,
            set, list, none
        item_min: int,
        item_max: int,

    }
    """
    _OOK_META = {}
