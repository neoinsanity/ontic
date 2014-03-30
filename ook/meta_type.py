"""The base class for deriving types that require schema support.


.. image:: images/object_types.jpg

Usage
------

Classes
--------

"""

from datetime import date, datetime, time

# The `type_map` converts the string declaration of attribute type.
TypeMap = {
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'list': list,
    'set': set,
    'str': basestring,
    'time': time,
    'date': date,
    'datetime': datetime,
}

# The `collection_type_set` is the set of supported collection types.
CollectionTypeSet = {dict, list, set}


class _CoreType(dict):
    """The root type of *Ook* types.

    **_CoreType** ensures that *Ook* objects can be access by either dict key
    or object attribute.

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

        Initializes the accessor behavior to allow for property access as
        dict key or object
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
