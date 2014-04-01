"""The **object_tools** provides the methods to create and validate **Ook**
types and objects.

Usage
======

There are two basic operations provided by **object_tools**; schema
definition and object
handling. Schema definition entails type creation and validation.

Schema Tools
-------------

To validate a schema definition, utilize the :meth:`~ook.object_tools
.validate_schema` method.

Schema are composed of :class:`~ook.object_type.PropertySchema` objects. If
there is a need,
individual **PropertySchema** objects can be validated individually with the
:meth:`~ook.object_tools.validate_property` method.

To create a python type for a given :class:`~ook.object_type.SchemaType`
utilize the
:meth:`~ook.object_tools.create_ook_type` method. **Ook** object instances
created by a generated
type are child classes of the :class:`~ook.object_types` class.

Object Tools
-------------

**Ook** objects created by either subclassing :class:`~ook.object_type
.BaseType` or via
:meth:`~create_ook_type`, will need to be validated. Utilize the
**Ook** object :meth:`~ook.object_tools.validate_object` method for validation.

If the need should arise for validation of an **Ook** object by value,
utilize the
:meth:`~ook.object_tools.validate_value` method.

"""

import meta_type
from ook.meta_type import SchemaProperty
from ook.object_type import BaseType
from schema_type import SchemaType

