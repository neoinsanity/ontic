from copy import copy, deepcopy


class CoreType(dict):
    """The root type of *Ontic* types.

    **CoreType** ensures that *Ontic* object properties can be accessed by
    either dict key or object attribute. For example::

    >>> some_object = CoreType({'key1': 'value1'})
    >>> assert some_object.key1 == 'value1'
    >>> assert some_object['key1'] == 'value1'
    >>> some_object.key2 = 'value2'
    >>> assert some_object['key2'] == 'value2'
    >>> some_object['key3'] = 'value3'
    >>> assert some_object.key3 == 'value3'
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

    def __del__(self):
        # The self reference is removed to promote fast garbage collection.
        self.__dict__ = None

    def __copy__(self):
        return type(self)(copy(dict(self)))

    def __deepcopy__(self, memo):
        the_copy = dict(self.__dict__)
        return type(self)(deepcopy(the_copy, memo))
