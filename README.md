Ook
====

**Objects of Knowledge**

Documentation
--------------

For the latest documentation, visist http://neoinsanity.github.io/ook/

Stable Ook and Installation
----------------------------

The latest stable release of Ook can be found on the master branch at
https://github.com/neoinsanity/ook/tree/master. For the latest release, use the develop branch at
https://github.com/neoinsanity/ook/tree/develop.

To install **Ook** utilize the *setup.py* method

  > python setup.py install

Project Development
--------------------

If you are interested in developing **Ook**, utilize the helper scripts to setup a dev
environment. Prior to running the dev setup scripts, ensure that you have *virtualenv* installed.
 All setup commands are assumed to be run from the project root,
 which is the directory containing the *setup.py* file.

Prep the development environment with the command:

  > bin/dev_setup.sh

This command will setup the virtualenv for the project in the directory */venv*. It will also
install the **Ook** in a develop mode, with the creation of a development egg file.

To run the unit tests:

  > bin/run_tests.sh

To run the documentation generation:

  > bin/doc_build.sh

