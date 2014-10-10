"""The setuptools setup file."""
from setuptools import setup

with open('README.txt') as file:
    long_description = file.read()

setup(
    name='ontic',
    version='0.0.3a',
    author='Raul Gonzalez',
    author_email='mindbender@gmail.com',
    url='https://github.com/neoinsanity/ontic',
    license='Apache License 2.0',
    description='Qualities and Quantities are the stuff of Objects.',
    long_description=long_description,
    packages=['ontic',],
    install_requires=[],
    include_package_data = True,
)
