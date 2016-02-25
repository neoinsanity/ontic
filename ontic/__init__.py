from typing import Union

from ontic import (ontic_core,
                   ontic_meta,
                   ontic_property,
                   ontic_schema,
                   ontic_class)

__all__ = ['ontic_core', 'ontic_property', 'ontic_schema', 'ontic_class']

# Type declaration for all ontic types. Used for type hinting.
OnticTypes = Union[ontic_property.OnticProperty,
                   ontic_schema.OnticSchema,
                   ontic_class.OnticClass]

__ONTIC_PROPERTY_BOOTSTRAP_SCHEMA__ = ontic_core.OnticCore({
    'type': ontic_core.OnticCore({
        'type': (str, type),  # todo: raul - this could be restricted list
        'default': None,
        'required': False,
        'enum': ontic_meta.TYPE_SET + (None,),
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'default': ontic_core.OnticCore({
        'type': None,
        'default': None,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'required': ontic_core.OnticCore({
        'type': bool,
        'default': False,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'enum': ontic_core.OnticCore({
        'type': set,
        'default': None,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'min': ontic_core.OnticCore({
        'type': tuple(ontic_meta.COMPARABLE_TYPES),
        'default': None,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'max': ontic_core.OnticCore({
        'type': tuple(ontic_meta.COMPARABLE_TYPES),
        'default': None,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'regex': ontic_core.OnticCore({
        'type': str,
        'default': None,
        'required': False,
        'enum': None,
        'min': 1,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'member_type': ontic_core.OnticCore({
        'type': (str, type),  # todo: raul - this could be restricted list
        #  subclass testing.
        'default': None,
        'required': False,
        'enum': ontic_meta.TYPE_SET + (None,),
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'member_min': ontic_core.OnticCore({
        'type': tuple(ontic_meta.COMPARABLE_TYPES),
        'default': None,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'member_max': ontic_core.OnticCore({
        'type': tuple(ontic_meta.COMPARABLE_TYPES),
        'default': None,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
})

# Bootstrap OnticProperty class with a schema definition.
ontic_property.OnticProperty.__set_schema_for_ontic_schema__(
    __ONTIC_PROPERTY_BOOTSTRAP_SCHEMA__)
