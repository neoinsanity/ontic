"""The setuptools setup file."""
from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='ontic',
    version='0.0.2',
    author='Raul Gonzalez',
    author_email='mindbender@gmail.com',
    url='http://neoinsanity.github.io/ook/',
    license='Apache License 2.0',
    description='Qualities and Quantities are the stuff of Objects.',
    long_description=long_description,
    packages=['ontic',],
    install_requires=[],
    include_package_data = True,
)
