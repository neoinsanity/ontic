"""The setuptools setup file.

"""

from setuptools import find_packages, setup

setup(
    name='ook',
    version='0.0.2',
    license='Apache License 2.0',
    description='Qualities and Quantities are the stuff of Objects.',
    packages=['ook',],
    install_requires=[],
    include_package_data = True,
)
