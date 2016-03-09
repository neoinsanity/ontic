from typing import Union

from ontic import (ontic_core,
                   ontic_meta,
                   ontic_property,
                   ontic_schema,
                   ontic_type)

__all__ = ['ontic_core', 'ontic_property', 'ontic_schema', 'ontic_type']

# Type declaration for all ontic types. Used for type hinting.
OnticTypes = Union[ontic_property.OnticProperty,
                   ontic_schema.Schema,
                   ontic_type.OnticType]
