"""The fundamental *Ook* base data types for creation of derived child classes.

Usage
------

The **object_type** module allows for the construction of **Ook** data types. A complete
configured data type definition would be constructed as::


    class MyType(BaseType):
        _OOK_SCHEMA = SchemaType({
            'some_property': PropertyType({
                'type': 'int',
                'required': True,
            }),
            'other_property': PropertyType({
                'type': 'str',
                'required': False,
                'enum': {'Enum1', 'Enum2', 'Enum3'}
            }),
        })

    my_object = MyType()
    my_object.some_property = 7
    # or
    my_object['some_property'] = 7


Classes
--------

"""

from core_type import MetaType


# The `type_map` converts the string declaration of attribute type.
TypeMap = {
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'list': list,
    'set': set,
    'str': basestring,
}

# The `collection_type_set` is the set of supported collection types.
CollectionTypeSet = {dict, list, set}


class BaseType(MetaType):
    """BaseType provides the **Ook** schema interface.

    The **BaseType** provides the schema management functionality to a derived **Ook** type
    instance.
    """



