"""The setuptools setup file.

"""

from setuptools import find_packages, setup

setup(
    name='ontic',
    version='0.0.1',
    license='Apache License 2.0',
    description='Qualities and Quantities are the stuff of Objects.',
    packages=['ontic',],
    install_requires=[],
    include_package_data = True,
)
