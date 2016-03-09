from typing import Union

from ontic import (core,
                   property,
                   schema,
                   type)
from ontic.property import OnticProperty
from ontic.schema import Schema
from ontic.type import OnticType

__all__ = ['OnticProperty', 'Schema', 'OnticType',
           'core', 'property', 'schema', 'type']

# Type declaration for all ontic types. Used for type hinting.
OnticTypes = Union[OnticProperty,
                   Schema,
                   OnticType]
