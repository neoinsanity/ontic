"""Testing suite for object_types module."""
from datetime import date, datetime, time

from test_utils import base_test_case

from ook import object_type
from ook.schema_type import SchemaType


class CreateOokTypeTestCase(base_test_case.BaseTestCase):
    """Test the dynamic creation of Ook types."""

    def test_create_ook_type_arg_errors(self):
        """Assert the create ook type arg errors."""
        self.assertRaisesRegexp(
            ValueError, 'The string "name" argument is required.',
            object_type.create_ook_type, name=None, schema=dict())
        self.assertRaisesRegexp(
            ValueError, 'The schema dictionary is required.',
            object_type.create_ook_type, name='SomeName', schema=None)
        self.assertRaisesRegexp(
            ValueError, 'The schema must be a dict.',
            object_type.create_ook_type, name='SomeName', schema=list())

    def test_create_ook_type(self):
        """The most simple and basic dynamic Ook."""
        # Test creation from raw dictionary.
        ook_type = object_type.create_ook_type('Simple', dict())

        self.assertIsNotNone(ook_type)

        ook_object = ook_type()
        self.assert_dynamic_accessing(ook_object)
        self.assertIsInstance(ook_object, ook_type)

        # Test creation using a SchemaType object.
        ook_type = object_type.create_ook_type('AnotherSimple', SchemaType())

        self.assertIsNotNone(ook_type)

        ook_object = ook_type()
        self.assert_dynamic_accessing(ook_object)
        self.assertIsInstance(ook_object, ook_type)


class ValidateObjectTestCase(base_test_case.BaseTestCase):
    """Test object_types.validate_object method basics."""

    def test_bad_validate_object(self):
        """ValueError testing of validate_object."""
        self.assertRaisesRegexp(
            ValueError,
            'Validation can only support validation of objects derived from '
            'ook.BaseType.',
            object_type.validate_object, None)
        self.assertRaisesRegexp(
            ValueError,
            'Validation can only support validation of objects derived from '
            'ook.BaseType.',
            object_type.validate_object, 'Not a BaseType')

    def test_type_setting(self):
        """Validate 'type' schema setting."""
        schema = {
            'bool_property': {'type': 'bool'},
            'dict_property': {'type': 'dict'},
            'float_property': {'type': 'float'},
            'int_property': {'type': 'int'},
            'list_property': {'type': 'list'},
            'set_property': {'type': 'set'},
            'str_property': {'type': 'str'},
            'date_property': {'type': 'date'},
            'time_property': {'type': 'time'},
            'datetime_property': {'type': 'datetime'},
        }

        # Create the type
        ook_type = object_type.create_ook_type('TypeCheck', schema)
        self.assertIsNotNone(ook_type)

        # Create object of type
        ook_object = ook_type()

        # Validate an empty object.
        object_type.validate_object(ook_object)

        # Validate with known good data.
        ook_object.bool_property = True
        ook_object.dict_property = {'some_key': 'some_value'}
        ook_object.float_property = 3.4
        ook_object.int_property = 5
        ook_object.list_property = [5, 6, 7]
        ook_object.set_property = {'dog', 'cat', 'mouse'}
        ook_object.str_property = 'some_string'
        ook_object.date_property = date(2000, 1, 1)
        ook_object.time_property = time(12, 30, 30)
        ook_object.datetime_property = datetime(2001, 1, 1, 12, 30, 30)
        object_type.validate_object(ook_object)

        # Validate with known bad data.
        ook_object.bool_property = 'Dog'
        self.assertRaisesRegexp(
            ValueError,
            'The value for "bool_property" is not of type "bool": Dog',
            object_type.validate_object, ook_object)
        ook_object.bool_property = True

        # Validate a string vs a list type
        ook_object.list_property = 'some_string'
        self.assertRaisesRegexp(
            ValueError,
            'The value for "list_property" is not of type "list": some_string',
            object_type.validate_object, ook_object)

    def test_type_bad_setting(self):
        """ValueError for bad 'type' setting."""
        schema = {
            'some_property': {'type': 'Unknown'}
        }
        # Create the type
        ook_type = object_type.create_ook_type('Dummy', schema)

        self.assertIsNotNone(ook_type)
        self.assertIsInstance(ook_type, type)
        self.assertDictEqual(
            {'some_property': {'default': False,
                               'enum': None,
                               'item_max': None,
                               'item_min': None,
                               'item_type': None,
                               'max': None,
                               'min': None,
                               'regex': None,
                               'required': False,
                               'type': 'Unknown'}},
            ook_type.get_schema())

    def test_required_setting(self):
        """Validate 'required' schema setting."""
        schema = {
            'some_property': {'required': True},
            'other_property': {'required': False}
        }

        # Create the type
        ook_type = object_type.create_ook_type('RequireCheck', schema)
        self.assertIsNotNone(ook_type)

        # Create object of type
        ook_object = ook_type()

        # Validate an empty object, which should cause ValueError
        self.assertRaisesRegexp(
            ValueError, 'The value for "some_property" is required.',
            object_type.validate_object, ook_object)

        # Validate with data
        ook_object.some_property = 'Something'
        ook_object.other_property = 'Other'
        object_type.validate_object(ook_object)

    def test_enum_setting(self):
        """Validate 'enum' schema setting."""
        # Scalar testing
        ################
        schema = {
            'enum_property': {'enum': {'some_value', 99}}
        }

        # Create the type
        ook_type = object_type.create_ook_type('EnumCheck', schema)
        self.assertIsNotNone(ook_type)

        # Create object of type
        ook_object = ook_type()

        # Validate an empty object
        object_type.validate_object(ook_object)

        # Validate a good setting
        ook_object.enum_property = 99
        object_type.validate_object(ook_object)

        # Validate a bad setting
        ook_object.enum_property = 'bad, bad, bad'
        self.assertRaisesRegexp(
            ValueError,
            "The value \"bad, bad, bad\" for \"enum_property\" "
            "not in enumeration \[99, 'some_value'\].",
            object_type.validate_object, ook_object)

        # Collection testing
        ####################
        schema = {
            'enum_property': {'type': 'list', 'enum': {'dog', 'cat'}}
        }

        # Create the type
        ook_type = object_type.create_ook_type('EnumListCheck', schema)
        self.assertIsNotNone(ook_type)

        # Create object of type
        ook_object = ook_type()

        # Validate an empty object
        object_type.validate_object(ook_object)

        # Validate a good setting
        ook_object.enum_property = ['dog']
        object_type.validate_object(ook_object)

        # Validate a bad setting
        ook_object.enum_property = ['fish']
        self.assertRaisesRegexp(
            ValueError,
            r'''The value "fish" for "\['fish'\]" not in enumeration '''
            r'''\['dog', 'cat'\].''',
            object_type.validate_object, ook_object)

    def test_min_setting(self):
        """Validate 'min' schema setting."""
        schema = {
            'str_min_property': {'type': 'str', 'min': 5},
            'int_min_property': {'type': 'int', 'min': 10},
            'float_min_property': {'type': 'float', 'min': 20},
            'list_min_property': {'type': 'list', 'min': 1},
            'set_min_property': {'type': 'set', 'min': 1},
            'dict_min_property': {'type': 'dict', 'min': 1},
            'date_min_property': {'type': 'date', 'min': date(2000, 1, 1)},
            'time_min_property': {'type': 'time', 'min': time(12, 30, 30)},
            'datetime_min_property': {
                'type': 'datetime', 'min': datetime(2000, 1, 1, 12, 30, 30)}
        }

        ook_type = object_type.create_ook_type('MinCheck', schema)
        self.assertIsNotNone(ook_type)

        ook_object = ook_type()

        # None test, with no required fields
        object_type.validate_object(ook_object)

        # Good test
        ook_object.str_min_property = '8 letters'
        ook_object.int_min_property = 20
        ook_object.float_min_property = 30.0
        ook_object.list_min_property = ['one item']
        ook_object.set_min_property = {'one item'}
        ook_object.dict_min_property = {'some_kee': 'one item'}
        ook_object.date_min_property = date(2001, 1, 1)
        ook_object.time_min_property = time(13, 30, 30)
        ook_object.datetime_min_property = datetime(2001, 1, 1)
        object_type.validate_object(ook_object)

        # Str failure
        ook_object.str_min_property = '1'
        self.assertRaisesRegexp(ValueError,
                                'The value of "1" for "str_min_property" '
                                'fails min of 5.',
                                object_type.validate_object, ook_object)
        ook_object.str_min_property = '8 letters'

        # Int failure
        ook_object.int_min_property = 5
        self.assertRaisesRegexp(ValueError,
                                'The value of "5" for "int_min_property" '
                                'fails min of 10.',
                                object_type.validate_object, ook_object)
        ook_object.int_min_property = 20

        # Float failure
        ook_object.float_min_property = 15.0
        self.assertRaisesRegexp(ValueError,
                                'The value of "15.0" for "float_min_property" '
                                'fails min of 20.',
                                object_type.validate_object, ook_object)
        ook_object.float_min_property = 30.0

        # List failure
        ook_object.list_min_property = list()
        self.assertRaisesRegexp(ValueError,
                                'The value of "\[]" for "list_min_property" '
                                'fails min of 1.',
                                object_type.validate_object, ook_object)
        ook_object.list_min_property = ['one item']

        # Set failure
        ook_object.set_min_property = set()
        self.assertRaisesRegexp(ValueError,
                                'The value of "set\(\[]\)" for '
                                '"set_min_property" fails min of 1.',
                                object_type.validate_object, ook_object)
        ook_object.set_min_property = {'one item'}

        # Dict failure
        ook_object.dict_min_property = dict()
        self.assertRaisesRegexp(ValueError,
                                'The value of "{}" for "dict_min_property" '
                                'fails min of 1.',
                                object_type.validate_object, ook_object)
        ook_object.dict_min_property = {'some_key': 'one_item'}

        # Date failure
        ook_object.date_min_property = date(1999, 1, 1)
        self.assertRaisesRegexp(ValueError,
                                'date_min_property" fails min of 2000-01-01.',
                                object_type.validate_object, ook_object)
        ook_object.date_min_property = date(2001, 1, 1)

        # Time failure
        ook_object.time_min_property = time(11, 30, 30)
        self.assertRaisesRegexp(
            ValueError,
            'The value of "11:30:30" for "time_min_property" '
            'fails min of 12:30:30.',
            object_type.validate_object, ook_object)
        ook_object.time_min_property = time(13, 30, 30)

        # Datetime failure
        ook_object.datetime_min_property = datetime(1999, 1, 1, 11, 30, 30)
        self.assertRaisesRegexp(
            ValueError,
            'The value of "1999-01-01 11:30:30" for "datetime_min_property" '
            'fails min of 2000-01-01 12:30:30.',
            object_type.validate_object, ook_object)

    def test_max_setting(self):
        """Validate 'max' schema setting."""
        schema = {
            'str_max_property': {'type': 'str', 'max': 5},
            'int_max_property': {'type': 'int', 'max': 10},
            'float_max_property': {'type': 'float', 'max': 20},
            'list_max_property': {'type': 'list', 'max': 1},
            'set_max_property': {'type': 'set', 'max': 1},
            'dict_max_property': {'type': 'dict', 'max': 1},
            'date_max_property': {'type': 'date', 'max': date(2000, 1, 1)},
            'time_max_property': {'type': 'time', 'max': time(12, 30, 30)},
            'datetime_max_property': {
                'type': 'datetime', 'max': datetime(2000, 1, 1, 12, 30, 30)}
        }

        ook_type = object_type.create_ook_type('MaxCheck', schema)
        self.assertIsNotNone(ook_type)
        #object_types.validate_schema(ook_type.get_schema())

        ook_object = ook_type()

        # None test, with no required fields
        object_type.validate_object(ook_object)

        # Good test
        ook_object.str_max_property = 'small'
        ook_object.int_max_property = 5
        ook_object.float_max_property = 10.0
        ook_object.list_max_property = ['one item']
        ook_object.set_max_property = {'one item'}
        ook_object.dict_max_property = {'some_kee': 'one item'}
        ook_object.date_max_property = date(1999, 1, 1)
        ook_object.time_max_property = time(11, 30, 30)
        ook_object.datetime_max_property = datetime(1999, 1, 1)
        object_type.validate_object(ook_object)

        # Str failure
        ook_object.str_max_property = '8 letters'
        self.assertRaisesRegexp(ValueError,
                                'The value of "8 letters" for '
                                '"str_max_property" fails max of 5.',
                                object_type.validate_object, ook_object)
        ook_object.str_max_property = 'small'

        # Int failure
        ook_object.int_max_property = 20
        self.assertRaisesRegexp(ValueError,
                                'The value of "20" for "int_max_property" '
                                'fails max of 10.',
                                object_type.validate_object, ook_object)
        ook_object.int_max_property = 5

        # Float failure
        ook_object.float_max_property = 30.0
        self.assertRaisesRegexp(
            ValueError,
            'The value of "30.0" for "float_max_property" fails max of 20.',
            object_type.validate_object, ook_object)
        ook_object.float_max_property = 15.0

        # List failure
        ook_object.list_max_property = ['one item', 'two item']
        self.assertRaisesRegexp(
            ValueError,
            'The value of "\[\'one item\', \'two item\'\]" '
            'for "list_max_property" fails max of 1.',
            object_type.validate_object, ook_object)
        ook_object.list_max_property = ['one item']

        # Set failure
        ook_object.set_max_property = {'one item', 'two item'}
        self.assertRaisesRegexp(
            ValueError,
            'The value of "set\(\[\'one item\', \'two item\'\]\)" '
            'for "set_max_property" fails max of 1.',
            object_type.validate_object, ook_object)
        ook_object.set_max_property = {'one item'}

        # Dict failure
        ook_object.dict_max_property = {'some_key': 'one_item',
                                        'another_key': 'two_item'}
        self.assertRaisesRegexp(
            ValueError,
            'The value of "{\'another_key\': \'two_item\', \'some_key\': '
            '\'one_item\'}" for '
            '"dict_max_property" fails max of 1.',
            object_type.validate_object, ook_object)
        ook_object.dict_max_property = {'some_key': 'one_item'}

        # Date failure
        ook_object.date_max_property = date(2001, 1, 1)
        self.assertRaisesRegexp(
            ValueError,
            'The value of "2001-01-01" for '
            '"date_max_property" fails max of 2000-01-01.',
            object_type.validate_object, ook_object)
        ook_object.date_max_property = date(2001, 1, 1)

        # Time failure
        ook_object.time_max_property = time(13, 30, 30)
        self.assertRaisesRegexp(
            ValueError,
            'The value of "13:30:30" for "time_max_property" '
            'fails max of 12:30:30.',
            object_type.validate_object, ook_object)
        ook_object.time_max_property = time(13, 30, 30)

        # Datetime failure
        ook_object.datetime_max_property = datetime(2001, 1, 1, 11, 30, 30)
        self.assertRaisesRegexp(
            ValueError,
            'The value of "2001-01-01 11:30:30" for "datetime_max_property" '
            'fails max of 2000-01-01 12:30:30.',
            object_type.validate_object, ook_object)

    def test_regex_setting(self):
        """Validate 'regex' schema setting."""
        schema = {
            'b_only_property': {'type': 'str', 'regex': '^b+'}
        }

        ook_type = object_type.create_ook_type('RegexCheck', schema)
        self.assertIsNotNone(ook_type)

        ook_object = ook_type()

        # None test, with no required fields
        object_type.validate_object(ook_object)

        # Good test
        ook_object.b_only_property = ''
        object_type.validate_object(ook_object)
        ook_object.b_only_property = 'b'
        object_type.validate_object(ook_object)

        # Bad test
        ook_object.b_only_property = 'a'
        self.assertRaisesRegexp(ValueError,
                                'Value \"a\" for b_only_property does not '
                                'meet regex: \^b\+',
                                object_type.validate_object, ook_object)

    def test_item_type_setting(self):
        """Validate 'item_type' setting."""
        schema = {
            'list_property': {'type': 'list', 'item_type': 'str'}
        }

        ook_type = object_type.create_ook_type('ItemTypeCheck', schema)
        self.assertIsNotNone(ook_type)

        ook_object = ook_type()

        # None test, with no required fields.
        object_type.validate_object(ook_object)

        # Good test
        ook_object.list_property = []
        object_type.validate_object(ook_object)
        ook_object.list_property.append('some_item')
        object_type.validate_object(ook_object)

        # Bad test
        ook_object.list_property.append(99)
        self.assertRaisesRegexp(
            ValueError,
            r'''The value for "\['some_item', 99\]" is not of type "str": 99''',
            object_type.validate_object, ook_object)

    def test_collection_regex_setting(self):
        """Validate string collection with 'regex' setting."""
        schema = {
            'set_property': {'type': 'set', 'item_type': 'str', 'regex': 'b+'}
        }

        ook_type = object_type.create_ook_type('CollectionRegexCheck', schema)
        self.assertIsNotNone(ook_type)

        ook_object = ook_type()

        # None test, with no required fields.
        object_type.validate_object(ook_object)

        # Good test
        ook_object.set_property = set()
        object_type.validate_object(ook_object)
        ook_object.set_property.add('bbbbb')
        object_type.validate_object(ook_object)

        # Bad test
        ook_object.set_property.add('xxxxxx')
        self.assertRaisesRegexp(
            ValueError,
            r'''Value "xxxxxx" for '''
            '''set\(\['xxxxxx', 'bbbbb'\]\) does not meet regex: b+''',
            object_type.validate_object, ook_object)

    def test_item_min_setting(self):
        """Validate 'item_min' setting."""
        # Test the item min setting for string items.
        schema = {
            'list_property': {'type': 'list', 'item_type': 'str', 'item_min': 4}
        }

        ook_type = object_type.create_ook_type('StrItemMinCheck', schema)
        self.assertIsNotNone(ook_type)

        ook_object = ook_type()

        # None test, with no required fields.
        object_type.validate_object(ook_object)

        # Good Test
        ook_object.list_property = []
        object_type.validate_object(ook_object)
        ook_object.list_property.append('four')
        object_type.validate_object(ook_object)

        # Bad Test
        ook_object.list_property.append('one')
        self.assertRaisesRegexp(
            ValueError,
            r'''The value of "one" for "\['four', 'one'\]" fails min of 4.''',
            object_type.validate_object, ook_object)

        # Test the item min setting for numeric items.
        schema = {
            'list_property': {'type': 'list', 'item_type': 'int', 'item_min': 4}
        }

        ook_type = object_type.create_ook_type('StrItemMinCheck', schema)
        self.assertIsNotNone(ook_type)

        ook_object = ook_type()

        # None test, with no required fields.
        object_type.validate_object(ook_object)

        # Good Test
        ook_object.list_property = []
        object_type.validate_object(ook_object)
        ook_object.list_property.append(4)
        object_type.validate_object(ook_object)

        # Bad Test
        ook_object.list_property.append(1)
        self.assertRaisesRegexp(
            ValueError,
            r'''The value of "1" for "\[4, 1\]" fails min of 4.''',
            object_type.validate_object, ook_object)

    def test_item_max_setting(self):
        """Validate 'item_max' setting."""
        # Test the item max setting for string items.
        schema = {
            'list_property': {
                'type': 'list', 'item_type': 'str', 'item_max': 4}
        }

        ook_type = object_type.create_ook_type('StrItemMinCheck', schema)
        self.assertIsNotNone(ook_type)

        ook_object = ook_type()

        # None test, with no required fields.
        object_type.validate_object(ook_object)

        # Good Test
        ook_object.list_property = []
        object_type.validate_object(ook_object)
        ook_object.list_property.append('four')
        object_type.validate_object(ook_object)

        # Bad Test
        ook_object.list_property.append('seven')
        self.assertRaisesRegexp(
            ValueError,
            r'''The value of "seven" for '''
            '''"\['four', 'seven'\]" fails max of 4.''',
            object_type.validate_object, ook_object)

        # Test the item min setting for numeric items.
        schema = {
            'list_property': {
                'type': 'list', 'item_type': 'int', 'item_max': 4}
        }

        ook_type = object_type.create_ook_type('StrItemMinCheck', schema)
        self.assertIsNotNone(ook_type)

        ook_object = ook_type()

        # None test, with no required fields.
        object_type.validate_object(ook_object)

        # Good Test
        ook_object.list_property = []
        object_type.validate_object(ook_object)
        ook_object.list_property.append(4)
        object_type.validate_object(ook_object)

        # Bad Test
        ook_object.list_property.append(7)
        self.assertRaisesRegexp(
            ValueError,
            r'''The value of "7" for "\[4, 7\]" fails max of 4.''',
            object_type.validate_object, ook_object)


class ValidateValueTestCase(base_test_case.BaseTestCase):
    """Test object_types.validate_value method."""

    def test_bad_validate_value(self):
        """ValueError testing of validate_value."""
        self.assertRaisesRegexp(
            ValueError,
            '"ook_object" is required, cannot be None.',
            object_type.validate_value, 'some_value', None)

        self.assertRaisesRegexp(
            ValueError,
            '"ook_object" must be BaseType or child type of BaseType',
            object_type.validate_value, 'some_value', "can't be string")

        ook_type = object_type.create_ook_type(
            'BadValidateValue',
            {
                'prop1': {'type': 'int'}
            })
        ook_object = ook_type()
        ook_object.prop1 = 1

        self.assertRaisesRegexp(
            ValueError,
            '"property_name" is required, cannot be None.',
            object_type.validate_value, None, ook_object)

        self.assertRaisesRegexp(
            ValueError,
            '"property_name" is not a valid string.',
            object_type.validate_value, '', ook_object)

        self.assertRaisesRegexp(
            ValueError,
            '"property_name" is not a valid string.',
            object_type.validate_value, 5, ook_object)

        self.assertRaisesRegexp(
            ValueError,
            '"property_name" is not a recognized property.',
            object_type.validate_value, 'illegal property name', ook_object)

        ook_object.prop1 = 'invalid string value'
        self.assertRaisesRegexp(
            ValueError,
            'The value for "prop1" is not of type "int": invalid string value',
            object_type.validate_value, 'prop1', ook_object)


    def test_validate_value_value_arg(self):
        """Valid value argument testing of validate_value."""
        # Test that scalar property is valid.
        single_property_schema = {
            'prop1': {'type': 'str'}
        }
        ook_type = object_type.create_ook_type(
            'GoodValidateValue', single_property_schema)
        ook_object = ook_type({'prop1': 'Hot Dog'})
        object_type.validate_value('prop1', ook_object)

