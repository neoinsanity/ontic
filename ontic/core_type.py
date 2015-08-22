"""The root class for the construction of **Ontic** implementation types.

.. image:: images/core_type.jpg

.. contents::

"""
from copy import copy, deepcopy


class CoreType(dict):
    """The root type of *Ontic* types.

    **CoreType** provides for *Ontic* object properties to be accessible as
    either dict key-value pairs or as object attributes.

    Example dict style and object style initialization::

    >>> some_object = CoreType({'key1': 'value1'}) # Dict style initialization
    >>> other_object = CoreType(key1='value1') # Object style initialization

    Example dict style and object style property access::

    >>> # Object attribute access to value
    >>> assert some_object.key1 == 'value1'
    >>> assert other_object.key1 == 'value1'
    >>> # Dict key access to value
    >>> assert some_object['key1'] == 'value1'
    >>> assert other_object['key1'] == 'value1'
    >>> # Dynamic property assignment is supported
    >>> some_object.key2 = 'value2' # Object value initialization
    >>> assert some_object['key2'] == 'value2'
    >>> other_object['key3'] = 'value3' # Dict style key-value assignment
    >>> assert other_object.key3 == 'value3'
    """

    def __init__(self, *args, **kwargs):
        r"""**CoreType** initialized as a `dict` type.

        Initializes the accessor behavior to allow for property access as
        dict key or object attribute.

        Dict Style Initialization
            CoreType() -> new empty CoreType

            CoreType(mapping) -> new CoreType initialized from a mapping
            object's (key, value) pairs

            CoreType(iterable) -> new CoreType initialized as if via::

                d = CoreType()
                for k, v in iterable:
                    d[k] = v

            CoreType(\*\*kwargs) -> new CoreType initialized with the
            name=value pairs in the keyword argument list.  For example::

                CoreType(one=1, two=2)
        """
        super(CoreType, self).__init__(*args, **kwargs)

        self.__dict__ = self

    def __copy__(self):
        return type(self)(copy(dict(self)))

    def __deepcopy__(self, memo):
        the_copy = dict(self.__dict__)
        return type(self)(deepcopy(the_copy, memo))
