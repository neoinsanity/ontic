"""The root class for the construction of *Ontic* implementation types.

.. image:: images/ontic_core.jpg

.. contents::

"""

from copy import copy, deepcopy


class OnticCore(dict):
    """The root type of *Ontic* types.
    
    **OnticCore** provides for *Ontic* object properties to be accessible as
    either dict key-value pairs or as object attributes. OnticCore also supports
    dict style intialization.

    Dict Style Initialization
        OnticCore() -> new empty OnticCore

        OnticCore(mapping) -> new OnticCore initialized from a mapping
        object's (key, value) pairs

        OnticCore(iterable) -> new OnticCore initialized as if via::

            d = OnticCore()
            for k, v in iterable:
                d[k] = v

        OnticCore(\*\*kwargs) -> new OnticCore initialized with the
        name=value pairs in the keyword argument list.  For example::

            OnticCore(one=1, two=2)
    
    Example dict style and object style initialization::

    >>> some_object = OnticCore({'key1': 'value1'}) # Dict style initialization
    >>> other_object = OnticCore(key1='value1') # Object style initialization

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
        super(OnticCore, self).__init__(*args, **kwargs)

        self.__dict__ = self

    def __copy__(self):
        return type(self)(copy(dict(self)))

    def __deepcopy__(self, memo):
        the_copy = dict(self.__dict__)
        return type(self)(deepcopy(the_copy, memo))
