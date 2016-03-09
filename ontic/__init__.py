from typing import Union

from ontic import (core,
                   meta,
                   property,
                   schema,
                   type)

__all__ = ['core.py', 'property.py', 'schema.py', 'type.py']

# Type declaration for all ontic types. Used for type hinting.
OnticTypes = Union[property.OnticProperty,
                   schema.Schema,
                   type.OnticType]
