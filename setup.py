"""The setuptools setup file."""
from setuptools import setup

# todo: raul - if the setup barfs on README.txt the use the setup.cfg file.as
# the tag is [metadata]/n description-file = README.md

with open('README.md') as file:
    long_description = file.read()

with open('VERSION') as version_file:
    version = version_file.read().strip()

setup(
    name='ontic',
    version=version,
    author='Raul Gonzalez',
    author_email='mindbender@gmail.com',
    url='https://github.com/neoinsanity/ontic',
    license='Apache License 2.0',
    description='Qualities and Quantities are the stuff of Objects.',
    long_description=long_description,
    packages=['ontic', ],
    install_requires=[],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
    ]
)
