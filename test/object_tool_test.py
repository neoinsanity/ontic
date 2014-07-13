"""Testing suite for ontic_types module."""
from datetime import date, datetime, time

from test_utils import base_test_case

from ontic import ontic_type
from ontic.schema_type import SchemaType
from ontic.validation_exception import ValidationException


class CreateOnticTypeTestCase(base_test_case.BaseTestCase):
    """Test the dynamic creation of Ontic types."""

    def test_create_ontic_type_arg_errors(self):
        """Assert the create ontic type arg errors."""
        self.assertRaisesRegexp(
            ValueError, 'The string "name" argument is required.',
            ontic_type.create_ontic_type, name=None, schema=dict())
        self.assertRaisesRegexp(
            ValueError, 'The schema dictionary is required.',
            ontic_type.create_ontic_type, name='SomeName', schema=None)
        self.assertRaisesRegexp(
            ValueError, 'The schema must be a dict.',
            ontic_type.create_ontic_type, name='SomeName', schema=list())

    def test_create_ontic_type(self):
        """The most simple and basic dynamic Ontic."""
        # Test creation from raw dictionary.
        my_type = ontic_type.create_ontic_type('Simple', dict())

        self.assertIsNotNone(my_type)

        ontic_object = my_type()
        self.assert_dynamic_accessing(ontic_object)
        self.assertIsInstance(ontic_object, my_type)

        # Test creation using a SchemaType object.
        my_type = ontic_type.create_ontic_type('AnotherSimple',
                                               SchemaType())

        self.assertIsNotNone(my_type)

        ontic_object = my_type()
        self.assert_dynamic_accessing(ontic_object)
        self.assertIsInstance(ontic_object, my_type)


class PerfectObjectTestCase(base_test_case.BaseTestCase):
    """Test ontic_type.perfect_object method."""

    def test_bad_perfect_usage(self):
        """Ensure handling of bad arguments to perfect)_object method."""
        self.assertRaisesRegexp(
            ValueError,
            r'"the_object" must be provided.',
            ontic_type.perfect_object, None)

        self.assertRaisesRegexp(
            ValueError,
            r'"the_object" must be OnticType type.',
            ontic_type.perfect_object, {})

    def test_valid_perfect_usage(self):
        """Ensure that the perfect behavior is correct."""
        schema_def = SchemaType({
            'prop_1': {'type': 'int'},
            'prop_2': {'type': 'int', 'default': 20},
            'prop_3': {'type': 'int', 'default': 30},
            'prop_4': {'type': 'int', 'default': 40},
        })
        my_type = ontic_type.create_ontic_type('PerfectOntic', schema_def)

        ontic_object = my_type()
        ontic_object.prop_1 = 1
        ontic_object.prop_3 = None
        ontic_object.prop_4 = 400
        ontic_object.extra_prop = 'Extra'

        expected_dict = {
            'prop_1': 1,
            'prop_2': 20,
            'prop_3': 30,
            'prop_4': 400
        }
        ontic_type.perfect_object(ontic_object)
        self.assertDictEqual(expected_dict, ontic_object)


class ValidateObjectTestCase(base_test_case.BaseTestCase):
    """Test ontic_types.validate_object method basics."""

    def test_bad_validate_object(self):
        """ValueError testing of validate_object."""
        self.assertRaisesRegexp(
            ValueError,
            'Validation can only support validation of objects derived from '
            'ontic.ontic_type.OnticType.',
            ontic_type.validate_object, None)
        self.assertRaisesRegexp(
            ValueError,
            'Validation can only support validation of objects derived from '
            'ontic.ontic_type.OnticType.',
            ontic_type.validate_object, 'Not a OnticType')

    def test_validation_exception_handling(self):
        """Ensure that validate_object handles error reporting."""
        schema_instance = SchemaType(some_attr={'type': 'int'})
        my_type = ontic_type.create_ontic_type('ValidateCheck',
                                               schema_instance)
        ontic_object = my_type()
        ontic_object.some_attr = 'WRONG'

        self.assertRaisesRegexp(
            ValidationException,
            r"""The value for "some_attr" is not of type "int": WRONG""",
            ontic_type.validate_object, ontic_object)

        expected_errors = [
            'The value for "some_attr" is not of type "int": WRONG']

        try:
            ontic_type.validate_object(ontic_object)
            self.fail('ValidationException should have been thrown.')
        except ValidationException as ve:
            self.assertListEqual(expected_errors, ve.validation_errors)

        errors = ontic_type.validate_object(ontic_object,
                                         raise_validation_exception=False)
        self.assertListEqual(expected_errors, errors)

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
        my_type = ontic_type.create_ontic_type('TypeCheck', schema)
        self.assertIsNotNone(ontic_type)

        # Create object of type
        ontic_object = my_type()

        # Validate an empty object.
        ontic_type.validate_object(ontic_object)

        # Validate with known good data.
        ontic_object.bool_property = True
        ontic_object.dict_property = {'some_key': 'some_value'}
        ontic_object.float_property = 3.4
        ontic_object.int_property = 5
        ontic_object.list_property = [5, 6, 7]
        ontic_object.set_property = {'dog', 'cat', 'mouse'}
        ontic_object.str_property = 'some_string'
        ontic_object.date_property = date(2000, 1, 1)
        ontic_object.time_property = time(12, 30, 30)
        ontic_object.datetime_property = datetime(2001, 1, 1, 12, 30, 30)
        ontic_type.validate_object(ontic_object)

        # Validate with known bad data.
        ontic_object.bool_property = 'Dog'
        self.assertRaisesRegexp(
            ValidationException,
            'The value for "bool_property" is not of type "bool": Dog',
            ontic_type.validate_object, ontic_object)
        ontic_object.bool_property = True

        # Validate a string vs a list type
        ontic_object.list_property = 'some_string'
        self.assertRaisesRegexp(
            ValidationException,
            'The value for "list_property" is not of type "list": some_string',
            ontic_type.validate_object, ontic_object)

    def test_type_bad_setting(self):
        """ValueError for bad 'type' setting."""
        schema = {
            'some_property': {'type': 'Unknown'}
        }

        self.assertRaisesRegexp(
            ValidationException,
            r"""The value "Unknown" for "type" not in enumeration \['set', """
            r"""'int', 'float', 'list', 'datetime', 'dict', 'str', 'time', """
            r"""'date', 'bool'\].""",
            ontic_type.create_ontic_type, 'Dummy', schema)

    def test_required_setting(self):
        """Validate 'required' schema setting."""
        schema = {
            'some_property': {'required': True},
            'other_property': {'required': False}
        }

        # Create the type
        my_type = ontic_type.create_ontic_type('RequireCheck', schema)
        self.assertIsNotNone(ontic_type)

        # Create object of type
        ontic_object = my_type()

        # Validate an empty object, which should cause ValueError
        self.assertRaisesRegexp(
            ValidationException,
            'The value for "some_property" is required.',
            ontic_type.validate_object, ontic_object)

        # Validate with data
        ontic_object.some_property = 'Something'
        ontic_object.other_property = 'Other'
        ontic_type.validate_object(ontic_object)

    def test_enum_setting(self):
        """Validate 'enum' schema setting."""
        # Scalar testing
        # ###############
        schema = {
            'enum_property': {'enum': {'some_value', 99}}
        }

        # Create the type
        my_type = ontic_type.create_ontic_type('EnumCheck', schema)
        self.assertIsNotNone(my_type)

        # Create object of type
        ontic_object = my_type()

        # Validate an empty object
        ontic_type.validate_object(ontic_object)

        # Validate a good setting
        ontic_object.enum_property = 99
        ontic_type.validate_object(ontic_object)

        # Validate a bad setting
        ontic_object.enum_property = 'bad, bad, bad'
        self.assertRaisesRegexp(
            ValidationException,
            "The value \"bad, bad, bad\" for \"enum_property\" "
            "not in enumeration \[99, 'some_value'\].",
            ontic_type.validate_object, ontic_object)

        # Collection testing
        # ###################
        schema = {
            'enum_property': {'type': 'list', 'enum': {'dog', 'cat'}}
        }

        # Create the type
        my_type = ontic_type.create_ontic_type('EnumListCheck', schema)
        self.assertIsNotNone(ontic_type)

        # Create object of type
        ontic_object = my_type()

        # Validate an empty object
        ontic_type.validate_object(ontic_object)

        # Validate a good setting
        ontic_object.enum_property = ['dog']
        ontic_type.validate_object(ontic_object)

        # Validate a bad setting
        ontic_object.enum_property = ['fish']
        self.assertRaisesRegexp(
            ValidationException,
            r'''The value "fish" for "enum_property" not in'''
            r''' enumeration \['cat', 'dog'\].''',
            ontic_type.validate_object, ontic_object)

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

        my_type = ontic_type.create_ontic_type('MinCheck', schema)
        self.assertIsNotNone(ontic_type)

        ontic_object = my_type()

        # None test, with no required fields
        ontic_type.validate_object(ontic_object)

        # Good test
        ontic_object.str_min_property = '8 letters'
        ontic_object.int_min_property = 20
        ontic_object.float_min_property = 30.0
        ontic_object.list_min_property = ['one item']
        ontic_object.set_min_property = {'one item'}
        ontic_object.dict_min_property = {'some_kee': 'one item'}
        ontic_object.date_min_property = date(2001, 1, 1)
        ontic_object.time_min_property = time(13, 30, 30)
        ontic_object.datetime_min_property = datetime(2001, 1, 1)
        ontic_type.validate_object(ontic_object)

        # Str failure
        ontic_object.str_min_property = '1'
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "1" for "str_min_property" '
            'fails min of 5.',
            ontic_type.validate_object, ontic_object)
        ontic_object.str_min_property = '8 letters'

        # Int failure
        ontic_object.int_min_property = 5
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "5" for "int_min_property" '
            'fails min of 10.',
            ontic_type.validate_object, ontic_object)
        ontic_object.int_min_property = 20

        # Float failure
        ontic_object.float_min_property = 15.0
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "15.0" for "float_min_property" '
            'fails min of 20.',
            ontic_type.validate_object, ontic_object)
        ontic_object.float_min_property = 30.0

        # List failure
        ontic_object.list_min_property = list()
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "\[]" for "list_min_property" '
            'fails min of 1.',
            ontic_type.validate_object, ontic_object)
        ontic_object.list_min_property = ['one item']

        # Set failure
        ontic_object.set_min_property = set()
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "set\(\[]\)" for '
            '"set_min_property" fails min of 1.',
            ontic_type.validate_object, ontic_object)
        ontic_object.set_min_property = {'one item'}

        # Dict failure
        ontic_object.dict_min_property = dict()
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "{}" for "dict_min_property" '
            'fails min of 1.',
            ontic_type.validate_object, ontic_object)
        ontic_object.dict_min_property = {'some_key': 'one_item'}

        # Date failure
        ontic_object.date_min_property = date(1999, 1, 1)
        self.assertRaisesRegexp(
            ValidationException,
            'date_min_property" fails min of 2000-01-01.',
            ontic_type.validate_object, ontic_object)
        ontic_object.date_min_property = date(2001, 1, 1)

        # Time failure
        ontic_object.time_min_property = time(11, 30, 30)
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "11:30:30" for "time_min_property" '
            'fails min of 12:30:30.',
            ontic_type.validate_object, ontic_object)
        ontic_object.time_min_property = time(13, 30, 30)

        # Datetime failure
        ontic_object.datetime_min_property = datetime(1999, 1, 1, 11, 30, 30)
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "1999-01-01 11:30:30" for "datetime_min_property" '
            'fails min of 2000-01-01 12:30:30.',
            ontic_type.validate_object, ontic_object)

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

        my_type = ontic_type.create_ontic_type('MaxCheck', schema)
        self.assertIsNotNone(ontic_type)

        ontic_object = my_type()

        # None test, with no required fields
        ontic_type.validate_object(ontic_object)

        # Good test
        ontic_object.str_max_property = 'small'
        ontic_object.int_max_property = 5
        ontic_object.float_max_property = 10.0
        ontic_object.list_max_property = ['one item']
        ontic_object.set_max_property = {'one item'}
        ontic_object.dict_max_property = {'some_kee': 'one item'}
        ontic_object.date_max_property = date(1999, 1, 1)
        ontic_object.time_max_property = time(11, 30, 30)
        ontic_object.datetime_max_property = datetime(1999, 1, 1)
        ontic_type.validate_object(ontic_object)

        # Str failure
        ontic_object.str_max_property = '8 letters'
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "8 letters" for '
            '"str_max_property" fails max of 5.',
            ontic_type.validate_object, ontic_object)
        ontic_object.str_max_property = 'small'

        # Int failure
        ontic_object.int_max_property = 20
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "20" for "int_max_property" '
            'fails max of 10.',
            ontic_type.validate_object, ontic_object)
        ontic_object.int_max_property = 5

        # Float failure
        ontic_object.float_max_property = 30.0
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "30.0" for "float_max_property" fails max of 20.',
            ontic_type.validate_object, ontic_object)
        ontic_object.float_max_property = 15.0

        # List failure
        ontic_object.list_max_property = ['one item', 'two item']
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "\[\'one item\', \'two item\'\]" '
            'for "list_max_property" fails max of 1.',
            ontic_type.validate_object, ontic_object)
        ontic_object.list_max_property = ['one item']

        # Set failure
        ontic_object.set_max_property = {'one item', 'two item'}
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "set\(\[\'one item\', \'two item\'\]\)" '
            'for "set_max_property" fails max of 1.',
            ontic_type.validate_object, ontic_object)
        ontic_object.set_max_property = {'one item'}

        # Dict failure
        ontic_object.dict_max_property = {'some_key': 'one_item',
                                          'another_key': 'two_item'}
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "{\'another_key\': \'two_item\', \'some_key\': '
            '\'one_item\'}" for '
            '"dict_max_property" fails max of 1.',
            ontic_type.validate_object, ontic_object)
        ontic_object.dict_max_property = {'some_key': 'one_item'}

        # Date failure
        ontic_object.date_max_property = date(2001, 1, 1)
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "2001-01-01" for '
            '"date_max_property" fails max of 2000-01-01.',
            ontic_type.validate_object, ontic_object)
        ontic_object.date_max_property = date(2001, 1, 1)

        # Time failure
        ontic_object.time_max_property = time(13, 30, 30)
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "13:30:30" for "time_max_property" '
            'fails max of 12:30:30.',
            ontic_type.validate_object, ontic_object)
        ontic_object.time_max_property = time(13, 30, 30)

        # Datetime failure
        ontic_object.datetime_max_property = datetime(2001, 1, 1, 11, 30, 30)
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "2001-01-01 11:30:30" for "datetime_max_property" '
            'fails max of 2000-01-01 12:30:30.',
            ontic_type.validate_object, ontic_object)

    def test_regex_setting(self):
        """Validate 'regex' schema setting."""
        schema = {
            'b_only_property': {'type': 'str', 'regex': '^b+'}
        }

        my_type = ontic_type.create_ontic_type('RegexCheck', schema)
        self.assertIsNotNone(ontic_type)

        ontic_object = my_type()

        # None test, with no required fields
        ontic_type.validate_object(ontic_object)

        # Good test
        ontic_object.b_only_property = ''
        ontic_type.validate_object(ontic_object)
        ontic_object.b_only_property = 'b'
        ontic_type.validate_object(ontic_object)

        # Bad test
        ontic_object.b_only_property = 'a'
        self.assertRaisesRegexp(
            ValidationException,
            'Value \"a\" for b_only_property does not '
            'meet regex: \^b\+',
            ontic_type.validate_object, ontic_object)

    def test_item_type_setting(self):
        """Validate 'member_type' setting."""
        schema = {
            'list_property': {'type': 'list', 'member_type': 'str'}
        }

        my_type = ontic_type.create_ontic_type('ItemTypeCheck', schema)
        self.assertIsNotNone(ontic_type)

        ontic_object = my_type()

        # None test, with no required fields.
        ontic_type.validate_object(ontic_object)

        # Good test
        ontic_object.list_property = []
        ontic_type.validate_object(ontic_object)
        ontic_object.list_property.append('some_item')
        ontic_type.validate_object(ontic_object)

        # Bad test
        ontic_object.list_property.append(99)
        self.assertRaisesRegexp(
            ValidationException,
            r'''The value "99" for "list_property" is not of type "str".''',
            ontic_type.validate_object, ontic_object)

    def test_collection_regex_setting(self):
        """Validate string collection with 'regex' setting."""
        schema = {
            'set_property': {'type': 'set', 'member_type': 'str', 'regex': 'b+'}
        }

        my_type = ontic_type.create_ontic_type('CollectionRegexCheck',
                                               schema)
        self.assertIsNotNone(ontic_type)

        ontic_object = my_type()

        # None test, with no required fields.
        ontic_type.validate_object(ontic_object)

        # Good test
        ontic_object.set_property = set()
        ontic_type.validate_object(ontic_object)
        ontic_object.set_property.add('bbbbb')
        ontic_type.validate_object(ontic_object)

        # Bad test
        ontic_object.set_property.add('xxxxxx')
        self.assertRaisesRegexp(
            ValidationException,
            r'''Value "xxxxxx" for "set_property" does not meet regex: b+''',
            ontic_type.validate_object, ontic_object)

    def test_item_min_setting(self):
        """Validate 'member_min' setting."""
        # Test the item min setting for string items.
        schema = {
            'list_property': {'type': 'list', 'member_type': 'str',
                              'member_min': 4}
        }

        my_type = ontic_type.create_ontic_type('StrItemMinCheck', schema)
        self.assertIsNotNone(ontic_type)

        ontic_object = my_type()

        # None test, with no required fields.
        ontic_type.validate_object(ontic_object)

        # Good Test
        ontic_object.list_property = []
        ontic_type.validate_object(ontic_object)
        ontic_object.list_property.append('four')
        ontic_type.validate_object(ontic_object)

        # Bad Test
        ontic_object.list_property.append('one')
        self.assertRaisesRegexp(
            ValidationException,
            r'''The value of "one" for "list_property" '''
            r'''fails min length of 4.''',
            ontic_type.validate_object, ontic_object)

        # Test the item min setting for numeric items.
        schema = {
            'list_property': {'type': 'list', 'member_type': 'int',
                              'member_min': 4}
        }

        my_type = ontic_type.create_ontic_type('StrItemMinCheck', schema)
        self.assertIsNotNone(ontic_type)

        ontic_object = my_type()

        # None test, with no required fields.
        ontic_type.validate_object(ontic_object)

        # Good Test
        ontic_object.list_property = []
        ontic_type.validate_object(ontic_object)
        ontic_object.list_property.append(4)
        ontic_type.validate_object(ontic_object)

        # Bad Test
        ontic_object.list_property.append(1)
        self.assertRaisesRegexp(
            ValidationException,
            r'''The value of "1" for "list_property" fails min size of 4.''',
            ontic_type.validate_object, ontic_object)

    def test_item_max_setting(self):
        """Validate 'member_max' setting."""
        # Test the item max setting for string items.
        schema = {
            'list_property': {
                'type': 'list', 'member_type': 'str', 'member_max': 4}
        }

        my_type = ontic_type.create_ontic_type('StrItemMinCheck', schema)
        self.assertIsNotNone(my_type)

        ontic_object = my_type()

        # None test, with no required fields.
        ontic_type.validate_object(ontic_object)

        # Good Test
        ontic_object.list_property = []
        ontic_type.validate_object(ontic_object)
        ontic_object.list_property.append('four')
        ontic_type.validate_object(ontic_object)

        # Bad Test
        ontic_object.list_property.append('seven')
        self.assertRaisesRegexp(
            ValidationException,
            r'''The value of "seven" for "list_property" '''
            r'''fails max length of 4.''',
            ontic_type.validate_object, ontic_object)

        # Test the item min setting for numeric items.
        schema = {
            'list_property': {
                'type': 'list', 'member_type': 'int', 'member_max': 4}
        }

        my_type = ontic_type.create_ontic_type('StrItemMinCheck', schema)
        self.assertIsNotNone(ontic_type)

        ontic_object = my_type()

        # None test, with no required fields.
        ontic_type.validate_object(ontic_object)

        # Good Test
        ontic_object.list_property = []
        ontic_type.validate_object(ontic_object)
        ontic_object.list_property.append(4)
        ontic_type.validate_object(ontic_object)

        # Bad Test
        ontic_object.list_property.append(7)
        self.assertRaisesRegexp(
            ValidationException,
            r'''The value of "7" for "list_property" fails max size of 4.''',
            ontic_type.validate_object, ontic_object)


class ValidateValueTestCase(base_test_case.BaseTestCase):
    """Test ontic_types.validate_value method."""

    def test_bad_validate_value(self):
        """ValueError testing of validate_value."""
        self.assertRaisesRegexp(
            ValueError,
            '"ontic_object" is required, cannot be None.',
            ontic_type.validate_value, 'some_value', None)

        self.assertRaisesRegexp(
            ValueError,
            '"ontic_object" must be OnticType or child type of OnticType',
            ontic_type.validate_value, 'some_value', "can't be string")

        my_type = ontic_type.create_ontic_type(
            'BadValidateValue',
            {
                'prop1': {'type': 'int'}
            })
        ontic_object = my_type()
        ontic_object.prop1 = 1

        self.assertRaisesRegexp(
            ValueError,
            '"property_name" is required, cannot be None.',
            ontic_type.validate_value, None, ontic_object)

        self.assertRaisesRegexp(
            ValueError,
            r'"property_name" is not a valid string.',
            ontic_type.validate_value, '', ontic_object)

        self.assertRaisesRegexp(
            ValueError,
            '"property_name" is not a valid string.',
            ontic_type.validate_value, 5, ontic_object)

        self.assertRaisesRegexp(
            ValueError,
            '"property_name" is not a recognized property.',
            ontic_type.validate_value, 'illegal property name', ontic_object)

    def test_validate_value_exception_handling(self):
        """Ensure validation exception handling by validation_object method."""
        schema_instance = SchemaType(some_attr={'type': 'int'})
        my_type = ontic_type.create_ontic_type('ValidateCheck',
                                               schema_instance)
        ontic_object = my_type()
        ontic_object.some_attr = 'WRONG'

        self.assertRaisesRegexp(
            ValidationException,
            r"""The value for "some_attr" is not of type "int": WRONG""",
            ontic_type.validate_value, 'some_attr', ontic_object)

        expected_errors = [
            'The value for "some_attr" is not of type "int": WRONG']

        try:
            ontic_type.validate_value('some_attr', ontic_object)
            self.fail('A ValidateException should have been thrown.')
        except ValidationException as ve:
            self.assertListEqual(expected_errors, ve.validation_errors)

        errors = ontic_type.validate_value('some_attr', ontic_object,
                                           raise_validation_exception=False)
        self.assertListEqual(expected_errors, errors)

    def test_validate_value_value_arg(self):
        """Valid value argument testing of validate_value."""
        # Test that scalar property is valid.
        single_property_schema = {
            'prop1': {'type': 'str'}
        }
        my_type = ontic_type.create_ontic_type(
            'GoodValidateValue', single_property_schema)
        ontic_object = my_type({'prop1': 'Hot Dog'})
        ontic_type.validate_value('prop1', ontic_object)
