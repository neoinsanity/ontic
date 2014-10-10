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

    ============ =============== ====================================
    Name         Type            Enumeration
    ============ =============== ====================================
    type         str             basestring, bool, complex, date,
                 type            datetime, dict, float, int, list,
                                 long, None, set, str, time, unicode
    default      None
    required     bool
    enum         set
    min          complex, date,
                 datetime,
                 float, int,
                 long, time
    max          complex, date,
                 datetime,
                 float, int,
                 long, time
    regex        str
    member_type  str             basestring, bool, complex, date,
                 type            datetime, dict, float, int, list,
                                 long, None, set, str, time, unicode
    member_min   complex, date,
                 datetime,
                 float, int,
                 long, time
    member_max   complex, date,
                 datetime,
                 float, int,
                 long, time
    ============ =============== ====================================

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

For a more extensive description of schema settings see
:ref:`property-schema-settings-table`

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

The *Person* class can now be used to create instances::

  person = Person(name='Sal', age=32, gender='M')
  # or
  person = Person({'name':'Sal', 'age':32, 'gender':'M'})
  # and also
  person = Person()
  person.name = 'Sal'
  person.age = 32
  person['gender'] = 'M'

Dynamic Type Definitions
-------------------------

It is also possible to define a type dynamically, with the use of the
*ontic.ontic_type.create_ontic_type* function. Such as::

  from ontic.ontic_type import create_ontic_type
  Person = create_ontic_type(
    'Person',
    {
      'name': {'type':'str', 'required':True, 'min':1},
      'age': {'type':'int', 'min':0},
      'gender': {'type':'str', 'enum':{'M','F','NA'}, 'default':'NA'},
    }
  )
  person = Person()

The *create_ontic_type* function also accepts a *SchemaType* as a schema
definition parameter.  As in::

  from ontic.ontic_type import create_ontic_type
  from ontic.schema_type import SchemaType
  schema = SchemaType({
    'name': {'type':'str', 'required':True, 'min':1},
    'age': {'type':'int', 'min':0},
    'gender': {'type':'str', 'enum':{'M','F','NA'}, 'default':'NA'},
  })
  Person = create_ontic_type('Person', schema)
  person = Person(name='Santos', height=)

Checkout the API documentation for *SchemaType* for advanced schema handling
features.

Working with Ontic Objects
===========================

Perfect
--------

Perfecting am *OnticType* instance, is to strip out any additional values that
may have been assigned to the object, and to ensure the existence of all
properties defined in the schema.

Perfecting an *OnticType* object is done with the
*ontic.ontic_type.perfect_object* function. Let's assume::

  class Person(OnticType):
    ONTIC_SCHEMA = SchemaType({
      'name': {'type': 'str', 'required': True, 'min': 1},
      'age': {'type': 'int', 'min': 0},
      'gender': {'type': 'str', 'enum': {'M','F', 'NA'}, 'default':'NA'},
    })

Then the following demonstrates the use of the *perfect_object* function::

  >>> person = Person(name='Santos',height=67)
  >>> person
  {'name': 'Santos', 'height': 67}
  >>> perfect_object(person)
  >>> person
  {'name': 'Santos', 'age': None, 'gender': 'NA'}

After being perfected the *person* object had the height property stripped.
The age and gender properties were added. The age property was set to None as
no default setting was provided. The gender property was defined with a
default setting, which was applied.

For the collection type (dict, list, set), the *perfect_object* method will
deepcopy the default value. This is to ensure that not all perfected objects
will share a pointer to the same collection instance.

Validate
---------

**Ontic** provides two methods for executing validation against a given
*OnticType* object, backed by a schema definition. There are the
*ontic.ontic_type.validate_object* and *ontic.ontic_type.validate_value*
functions. Both function will throw a
*ontic.validation_exception.ValidateException*, if an validation exception is
found.

For the validation examples, assume::

  class Person(OnticType):
    ONTIC_SCHEMA = SchemaType({
      'name': {'type': 'str', 'required': True, 'min': 1},
      'age': {'type': 'int', 'min': 0},
      'gender': {'type': 'str', 'enum': {'M','F', 'NA'}, 'default':'NA'},
    })

To validate an *OnticType* instance::

  >>> person = Person(age=-1,gender='W')
  >>> from ontic.ontic_type import validate_object
  >>> validate_object(person)
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "ontic/ontic_type.py", line 174, in validate_object
      raise ValidationException(value_errors)
  ontic.validation_exception.ValidationException: The value "W" for "gender"
  not in enumeration ['NA', 'M', 'F'].
  The value for "name" is required.

The *ValidationException* that is raised will attempt to exhaustively
determine all validation failures. The *ValidationException.message* will list
the validation failures as a new-line delimited list. There is also a list of
strings available from the *ValidationException.validation_errors* for
structured access to the validation failures. To demonstrate::

  >>> try:
  ...     validate_object(person)
  ... except ValidationException as ve:
  ...     ve.message
  ...     ve.validation_errors
  'The value "W" for "gender" not in enumeration [\'NA\', \'M\', \'F\']. \nThe value for "name" is required.'
  ['The value "W" for "gender" not in enumeration [\'NA\', \'M\', \'F\'].', 'The value for "name" is required.']

The *validate_value* function operates over a single property by passing a
key name for the property. Example::

  >>> person = Person(age=-1,gender='W')
  >>> from ontic.ontic_type import validate_value
  >>> validate_value('gender', person)
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "ontic/ontic_type.py", line 174, in validate_object
      raise ValidationException(value_errors)
  ontic.validation_exception.ValidationException: The value "W" for "gender"
  not in enumeration ['NA', 'M', 'F'].

Both the *validate_object* and *validate_value* functions provide the
*raise_validation_exception* parameter. If the *raise_validation_exception*
parameter is set to False, then the functions will return a list of value
failures. Demonstrated by::

  >>> validate_object(person, raise_validation_exception=False)
  ['The value "W" for "gender" not in enumeration [\'NA\', \'M\', \'F\'].',
  'The value for "name" is required.']
