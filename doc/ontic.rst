.. _getting-started-with-ontic:

===========================
Getting Started with Ontic
===========================

.. image:: images/ontic.jpg

.. contents::

Creating a Simple OnticType Object
===================================

**Ontic** objects strive to provide all the benefits of utilizing a Python dict
object, with the benefits of having class-like attributes for data access.
The default behavior of an **Ontic** object to to be a schema-less dictionary.
The example for the simplest **Ontic** object is::

  >>> from ontic.ontic_type import OnticType
  >>> my_object = OnticType()
  >>> my_object['some_property'] = 'Some value'
  >>> my_object.other_property = 3
  >>> my_object

The ability to use *OnticType* objects as dict, makes it easy to utilize with
most common interfaces. Here is an *OnticType* object with pymongo::

  >>> from ontic.ontic_type import OnticType
  >>> from pymongo import MongoClient
  >>> client = MongoClient()
  >>> persons = client.a_database.persons
  >>> person = OnticType()
  >>> person.name = 'My Name'
  >>> person.age = 32
  >>> person.id = persons.insert(person)


Dict Style Initialization
--------------------------

*OnticType* objects can be instantiated in the same fashion as a *dict* type.

    OnticType() -> new empty OnticType

    OnticType(mapping) -> new OnticType initialized from a mapping
    object's (key, value) pairs. For example, a dict object::

      o = OnticType({'p':'v'})

    OnticType(iterable) -> new OnticType initialized as if via::

      d = OnticType()
      for k, v in iterable:
        d[k] = v

    OnticType(\*\*kwargs) -> new OnticType initialized with the
    name=value pairs in the keyword argument list.  For example::

      OnticType(one={. . .}, two={. . .})

Creation of Ontic Types
========================

The steps for creating an *OnticType*, beyond the simplistic use case,
begins with *SchemaType* definition. *SchemaType* definitions are used to
create *OnticType* instances that can be perfected and validated.
**Ontic** provides methods for perfecting and validating *OnticType*
instances that have a *SchemaType* definition.

The following sections will demonstrate how to create *SchemaType* defined
*OnticType* instances.

Creation of Schema Definitions
-------------------------------

Here is the list of schema definition properties provided by **Ontic**.

.. table:: Property Schema Settings

  ============ ====== ======== ========  =================================
  name         type   default  required  enum
  ============ ====== ======== ========  =================================
  type         str    None     False     bool, dict, float, int,
                                         list, set, str, date, , datetime
  default      None   None     False     None
  required     bool   False    False     None
  enum         set    None     False     None
  min          float  None     False     None
  max          float  None     False     None
  regex        str    None     False     None
  member_type  str    None     False     bool, dict, float, int,
                                         list, set, str, date, , datetime
  member_min   float  None     False     None
  member_max   float  None     False     None
  ============ ====== ======== ========  =================================

The schema type settings are utilized to create a *SchemaType*::

  >>> from ontic.schema_type import SchemaType
  >>> my_schema = SchemaType(p={'type'='str', 'default'='NotAssigned')

The created schema type defines that an object should have a property *p*. In
addition the property *p* has a default value of "NotAssigned".

A more complex example::

  >>> from ontic.schema_type import SchemaType
  >>> person_schema = SchemaType({
  ...   'name': {'type': 'str', 'required': True, 'min': 1},
  ...   'age': {'type': 'int', 'min': 0},
  ...   'gender': {'type': 'str', 'enum': {'M','F', 'NA'}, 'default':'NA'},
  ... })

Below is a more extensive description of the behavior of each of the schema
type settings.

*type*
    The *type* settings restricts a property to a known type. If no type is
    defined, then any value type maybe assigned to the property.
*default*
    If the value is of a property is ``None``, then the default value is
    applied to the property during validation. Note: the default value is
    only applied to an instance during instance creation, or when a call to
    :meth:`perfect_schema_property`. The default is not applied during
    validation.
*required*
    A *PropertySchema* with a required setting of *True*, will fail
    validation if the property value is *None*.
*enum*
    An *enum* setting is a set of values that the property value must adhere
    to. If the *type* setting is provided, then the choices provided by
    *enum* must be of that type. If no *type* is provided, then the choices
    in the *enum* set may be of any type, even mixed type.
*min*
    The *min* setting has differing behavior, based on the *type* setting. If
    no *type* setting is provided, then *min* test will not occur. For the
    boundable types (str, list, dict, set) the *min* setting will test that
    the value length is not less than the minimum. For the comparable types
    (int, float, data, time, datatime) the *min* setting will test that the
    value is not less than the minimum.
*max*
    The *max setting has differing behavior, based on the *type* setting. If
    no *type* setting is provided, the *max* test will not occur. For the
    boundable types (str, list, dict, set) the *max* setting will test that
    the value length is not more than the maximum. For the comparable types
    (int, float, date, time, datetime) the *max* setting will test that the
    value is not more than the maximum.
*regex*
    The *regex* setting is only tested if the *type* or *member_type* setting
    is 'str' and the *regex* setting is not None. When active, the *regex*
    setting will be used to test the given string value.  If the property
    value is 'None', then no regex testing will be done.
*member_type*
    The *member_type* setting is used to restrict the value type for property
    *type* 'list' or 'set'. It does so ensuring that each member of the
    collection is of the type designated by *member_type*.
*member_min*
    The *member_min* setting has differing behavior, based on the
    *member_type* setting. If no *member_type* setting is provided, then
    *member_min* test will not occur. For the boundable types
    (str, list, dict, set), the *member_min* setting will test that the
    value length is not less than the minimum. For the comparable types
    (int, float, date, time, datetime) the *member_minimum* setting will test
    that the value is not less than the minimum.
*member_max*
    The *member_max* setting has differing behavior, based on the
    *member_max* setting. If no *member_type* setting is provided,
    then *member_max* test will not occur. For the boundable types
    (str, list, dict, set), the *member_max* setting will test that the
    value length is not more than the maximum. For the comparable types
    (int, float, date, time, datetime) the *member_max* setting will test
    that the value is not more than the maximum.


Class-style Type Definitions
-----------------------------

To declare a *OnticType* with a *SchemaType* definition,
you need to set the *ONTIC_SCHEMA* class attribute with a *SchemaType*
instance. Such as::

  class Person(OnticType):
    ONTIC_SCHEMA = SchemaType({
      'name': {'type': 'str', 'required': True, 'min': 1},
      'age': {'type': 'int', 'min': 0},
      'gender': {'type': 'str', 'enum': {'M','F', 'NA'}, 'default':'NA'},
    })

The *Person* class can not be used to create instances::

  person = Person(name='Sal', age=32, gender='M')
  # or
  person = Person({'name':'Sal', 'age':32, 'gender':'M'})
  # and also
  person = Person()
  person.name = 'Sal'
  person.age = 32
  person.gender = 'M'

Dynamic Type Definitions
-------------------------

Working with Ontic Objects
===========================
