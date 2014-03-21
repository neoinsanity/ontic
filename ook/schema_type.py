from core_type import MetaType
import schema_tools

class SchemaProperty(MetaType):
    """The object type for representing Property schema definitions.

    *Property Schema Settings*:

        *type*
            datetime*, date*, time*, str, int, float, bool, dict, set, list, none. Defaults to
            None.
        *required*
            True|False. Defaults False.
        *min*
            float. Defaults to None.
        *max*
            float. Defaults to None.
        *regex*
            string. Defaults to None.
        *item_type*
            datetime*, date*, time*, str, int, float, bool, dict, set, list, none. Default to None.
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
            'required': False,
            'enum': {'bool', 'dict', 'float', 'int', 'list', 'set', 'str'}
        }),
        'required': MetaType({
            'type': 'bool',
            'required': False,
        }),
        'enum': MetaType({
            'type': 'set',
            'required': False,
        }),
        'min': MetaType({
            'type': float,
            'required': False,
        }),
        'max': MetaType({
            'type': float,
            'required': False,
        }),
        'regex': MetaType({
            'type': 'str',
            'required': False,
            'min': 1,
        }),
        'item_type': MetaType({
            'type': 'str',
            'required': False,
            'enum': {'bool', 'dict', 'float', 'int', 'list', 'set', 'str'}
        }),
        'item_min': MetaType({
            'type': float,
            'required': False,
        }),
        'item_max': MetaType({
            'type': float,
            'required': False,
        }),
    })

    def __init__(self, *args, **kwargs):
        print '==== schema_property.args:', args
        print '==== schema_property.kwargs:', kwargs
        MetaType.__init__(self, *args, **kwargs)
        schema_tools.validate_schema_property(self)
        # for key in self.keys():
        #     print '======== key:', key
        #     #self[key] = SchemaProperty(self[key])
        # print '==== schema_property init done.'


class SchemaType(MetaType):
    """The type definition for a schema object.

    The **SchemaType** contains a dictionary of property field names and the corresponding
    **SchemaProperty** definition.

    Example SchemaType representation::

        SchemaType({
          'some_property': SchemaProperty({
                'type': 'str',
                'required': True
            })
        })
    """

    def __init__(self, *args, **kwargs):
        print '====== args:', args
        print '====== kwargs:', kwargs
        MetaType.__init__(self, *args, **kwargs)
        for key in self.keys():
            self[key] = SchemaProperty(self[key])

