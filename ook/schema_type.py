from core_type import MetaType


class SchemaProperty(MetaType):
    """The object type for representing Property schema definitions.

    *Property Schema Settings*:

        *type*
            datetime*, date*, time*, str, int, float, bool, dict, set, list,
            none. Defaults to None.
        *required*
            True|False. Defaults False.
        *min*
            float. Defaults to None.
        *max*
            float. Defaults to None.
        *regex*
            string. Defaults to None.
        *item_type*
            datetime*, date*, time*, str, int, float, bool, dict, set, list,
            none. Default to None.
        *tem_min*
            float. Defaults to None.
        *item_max*
            float, Defaults to None.

    \* - Are to be added in subsequent versions.
    """
    #: todo: Add support for datetime, date & time
    _OOK_SCHEMA = MetaType({
        'type': MetaType({
            'type': 'str',
            'default': None,
            'required': True,
            'enum': {'bool', 'dict', 'float', 'int', 'list', 'set', 'str'},
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'default': MetaType({
            'type': 'bool',
            'default': False,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'required': MetaType({
            'type': 'bool',
            'default': False,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'enum': MetaType({
            'type': 'set',
            'default': None,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'min': MetaType({
            'type': float,
            'default': None,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'max': MetaType({
            'type': float,
            'default': None,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'regex': MetaType({
            'type': 'str',
            'default': None,
            'required': True,
            'enum': None,
            'min': 1,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'item_type': MetaType({
            'type': 'str',
            'default': None,
            'required': True,
            'enum': {'bool', 'dict', 'float', 'int', 'list', 'set', 'str'},
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'item_min': MetaType({
            'type': float,
            'default': None,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
        'item_max': MetaType({
            'type': float,
            'default': None,
            'required': True,
            'enum': None,
            'min': None,
            'max': None,
            'regex': None,
            'item_type': None,
            'item_min': None,
            'item_max': None,
        }),
    })

    def __init__(self, *args, **kwargs):
        MetaType.__init__(self, *args, **kwargs)

        import schema_tools

        schema_tools.perfect_schema_property(self)
        schema_tools.validate_schema_property(self)


class SchemaType(MetaType):
    """The type definition for a schema object.

    The **SchemaType** contains a dictionary of property field names and
    the corresponding **SchemaProperty** definition.

    Example SchemaType representation::

        SchemaType({
          'some_property': SchemaProperty({
                'type': 'str',
                'required': True
            })
        })
    """

    def __init__(self, *args, **kwargs):
        MetaType.__init__(self, *args, **kwargs)
        for key, value in self.iteritems():
            if not isinstance(value, SchemaProperty):
                self[key] = SchemaProperty(value)

