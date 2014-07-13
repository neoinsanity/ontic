============
Ontic 0.0.2
============

Welcome to **Ontic**, a package designed with making it easy to handle data 
objects. **Ontic** provides a pure data object representations that support 
*object-style* and *dict-style* attribute access. In addition, **Ontic** 
supports schema definition to aid in the validation and management of **Ontic**
object instances.

By way of a quick preview:

  > from ontic.ontic_type import OnticType, create_ontic_type, validate_object
  > from ontic.schema_type import SchemaType
  # Define the schema
  schema = SchemaType(
    prop1={'type':'str','required':True},
    prop2={'type':'int','min':1}) 
  # Define an ontic type
  AType = create_ontic_type('AType', schema)
  # Use AType to create a data instance
  obj = AType()
  # Show off object and dict style property access
  obj.prop1 = 'Some Value'
  obj['prop2'] = 3
  # And the validation
  validate_object(obj)

Documentation
==============

For the latest documentation, visit http://neoinsanity.github.io/ontic/

Getting Ontic
==============

Installation
-------------

Use pip to install ontic.

  > pip install ontic
  
Source
-------

The latest stable release source of **Ontic** can be found on the master 
branch at https://github.com/neoinsanity/ontic/tree/master. 

For the latest development code, use the develop branch at 
https://github.com/neoinsanity/ontic. Please note that the development branch
may change without notification.

To install **Ontic** from source utilize the *setup.py*:

  > python setup.py install

Project Development
====================

If you are interested in developing **Ontic** code, 
utilize the helper scripts in the *ontic/bin* directory.

Setup the Development Environment
----------------------------------

Prior to running the dev setup scripts, ensure that you have *virtualenv* 
installed. All setup commands are assumed to be run from the project root, 
which is the directory containing the *setup.py* file.

Prep the development environment with the command:

  > bin/dev_setup.sh

This command will setup the virtualenv for the project in the 
directory */venv*. It will also install the **Ontic** in a develop mode, 
with the creation of a development egg file.

Enable the Development Environment
-----------------------------------

To make it easy to ensure a correctly configured development session, 
utilize the command:

  > . bin/enable_dev.sh
  
or

  > source bin/enable_dev.sh
  
Note that the script must be sourced, as it will enable a virtualenv session 
and add the *bin* directory scripts to environment *PATH*.

Running Tests
--------------

To run the unit tests:

  > run_tests.sh

Building Documentation
-----------------------

To run the documentation generation:

  > doc_build.sh

