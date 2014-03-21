

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


class MetaType(_CoreType):
    #: The Ook schema pointer.
    _OOK_SCHEMA = None

    @classmethod
    def get_schema(cls):
        """Returns the **SchemaType** instance for a given **Ook** type.

        :return: The schema metadata definition for the BaseType derived
            child type.
        :rtype: ook.object_type.SchemaType.
        """
        return cls._OOK_SCHEMA
