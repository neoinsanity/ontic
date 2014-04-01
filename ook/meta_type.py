"""The base class for deriving types that require schema support.


.. image:: images/object_types.jpg

Usage
------

"""

from datetime import date, datetime, time

#: The `TYPE_MAP` converts the string declaration of attribute type.
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

#: The `SUPPORTED_COLLECTION_TYPES` is the set of supported collection types.
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
