=============================================================
Ontic - of or relating to entities and the facts about them
=============================================================

The goal of **Ontic** is to provide a pure data object that is flexible to use in
a python project. The motivation is to make it simple to utilize in a
development environment that interfaces with external services and
third-party tools, but not require an extensive library to convert objects.

To that end **Ontic** objects can be accessed through attribute access or via
dictionary key access. The theory is that most third party libraries, from JSON
to NoSql packages, take some form of the dict as input. Attribute access is
easier to type when writing code, hence the attribute access. By way of
example::

  >>> an_object = ontic.ontic_type.OnticType()
  >>> an_object['property1'] = 1
  >>> assert an_object.property1 == 1
  >>> an_object.property2 = 2
  >>> assert an_object['property2] == 2
  >>> json.dumps(an_object)  # an_object implements dict.
    '{"property1": 1, "property2": 2}'

As **Ontic** objects are designed to be utilized as pure data objects, they
implement the python *dict* interface. So anywhere you can use or pass a dict
object, you can pass an **Ontic** object. **Ontic** objects can even be
initialized like a dictionary, as exampled below::

  >>> an_object = ontic.ontic_type.OnticType({'the_property':'the_value'})
  >>> assert an_object.the_property = 'the_value'
  >>> assert an_object['the_property'] = 'the_value'

In addition **Ontic** provides schema and validation features to aid in working
with data representations. Schemas and corresponding types can be generated
at runtime, or types can be defined as classes that derive from the **Ontic**
*OnticType*. Here's some quick examples::

  Class definition of an Ontic type with schema.
  >>> from ontic.ontic_type import OnticType
  >>> from ontic_schema_type import SchemaType
  >>> class MyType(OnticType):
  ...   ONTIC_SCHEMA = SchemaType({'the_property':{'required':True}})
  >>> my_object = MyType()
  >>> ontic.ontic_type.validate_object(my_object)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "ontic/ontic_type.py", line 137, in validate_object
        raise ValidationException(str.join(' \n-- ', value_errors))
    ValidationException: The value for "the_property" is required.
  >>> my_object.the_property = 99
  >>> ontic.ontic_type.validate_object(my_object)

and dynamic definition of Ontic type with schema.

  >>> my_type = ontic.ontic_type.create_ontic_type(
  ...   'MyType', {'the_property':{'required':True}})
  >>> my_object = my_type()
  >>> ontic.ontic_type.validate_object(my_object)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "ontic/ontic_type.py", line 137, in validate_object
        raise ValueError(str.join(' \n-- ', value_errors))
    ValidationException: The value for "the_property" is required.
  >>> my_object['the_property'] = 'Some value'
  >>> ontic.ontic_type.validate_object(my_object)

For full coverage of schema definitions and usage details,
see :ref:`getting-started-with-ontic`.

.. warning::
    The limitation to this approach is that **Ontic** objects should not be
    monkey patched with any public methods.

*Share and Enjoy*.

Usage Documentation
--------------------
.. toctree::
  :maxdepth: 3

  ontic

API Specification
------------------
.. toctree::
  :maxdepth: 3

  ontic.core_type
  ontic.meta_type
  ontic.ontic_type
  ontic.schema_type
  ontic.validation_exception


Indices and Tables
===================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

