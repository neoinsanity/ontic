"""Test the basic functionality of the base and core data types."""
from datetime import date, time, datetime

from test.utils import BaseTestCase

from ontic.meta import Meta
from ontic import type as o_type
from ontic import OnticType
from ontic import property
from ontic.property import OnticProperty
from ontic.schema import Schema
from ontic.validation_exception import ValidationException


class OnticTypeTest(BaseTestCase):
    """OnticType test cases."""

    def test_object_type_instantiation(self):
        """OnticType instantiation to confirm dict behavior"""
        schema = {'prop': {'type': 'int'}}
        my_type = o_type.create_ontic_type('MyType', schema)

        expected_dict = {'prop': 3}

        my_object = my_type()
        my_object.prop = 3
        self.assertDictEqual(expected_dict, my_object)

    def test_dynamic_access(self):
        """OnticType property access as a Dict and an Attribute."""
        some_type = o_type.OnticType()
        self.assert_dynamic_accessing(some_type)

    def test_ontic_type_perfect(self):
        """Test the OnticType.perfect method."""
        schema_def = Schema({
            'prop_1': {'type': 'int'},
            'prop_2': {'type': 'int', 'default': 20},
            'prop_3': {'type': 'int', 'default': 30},
            'prop_4': {'type': 'int', 'default': 40},
        })
        my_type = o_type.create_ontic_type('PerfectOntic', schema_def)

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
        ontic_object.perfect()
        self.assertDictEqual(expected_dict, ontic_object)

    def test_ontic_type_validate(self):
        """Test the OnticType.validate method."""
        schema = {
            'some_property': {'required': True},
            'other_property': {'required': False}
        }

        # Create the o_type
        my_type = o_type.create_ontic_type('RequireCheck', schema)
        self.assertIsNotNone(o_type)

        # Create object of o_type
        ontic_object = my_type()

        # Validate an empty object, which should cause ValueError
        self.assertRaisesRegexp(
            ValidationException,
            'The value for "some_property" is required.',
            ontic_object.validate)

        # Validate with data
        ontic_object.some_property = 'Something'
        ontic_object.other_property = 'Other'
        o_type.validate_object(ontic_object)

    def test_object_type_validate_value(self):
        """Test ObjectType.validate_value method."""
        # Test that scalar property is valid.
        single_property_schema = {
            'prop1': {'type': 'str'}
        }
        my_type = o_type.create_ontic_type(
            'GoodValidateValue', single_property_schema)
        ontic_object = my_type({'prop1': 'Hot Dog'})
        self.assertEqual([], ontic_object.validate_value('prop1'))


class CreateOnticTypeTestCase(BaseTestCase):
    """Test the dynamic creation of Ontic types."""

    def test_create_ontic_type_arg_errors(self):
        """Assert the create ontic o_type arg errors."""
        self.assertRaisesRegexp(
            ValueError, 'The string "name" argument is required.',
            o_type.create_ontic_type, name=None, schema=dict())
        self.assertRaisesRegexp(
            ValueError, 'The schema dictionary is required.',
            o_type.create_ontic_type, name='SomeName', schema=None)
        self.assertRaisesRegexp(
            ValueError, 'The schema must be a dict.',
            o_type.create_ontic_type, name='SomeName', schema=list())

    def test_create_ontic_type(self):
        """The most simple and basic dynamic Ontic."""
        # Test creation from raw dictionary.
        my_type = o_type.create_ontic_type('Simple', dict())

        self.assertIsNotNone(my_type)

        ontic_object = my_type()
        self.assert_dynamic_accessing(ontic_object)
        self.assertIsInstance(ontic_object, my_type)

        # Test creation using a Schema object.
        my_type = o_type.create_ontic_type('AnotherSimple', Schema())

        self.assertIsNotNone(my_type)

        ontic_object = my_type()
        self.assert_dynamic_accessing(ontic_object)
        self.assertIsInstance(ontic_object, my_type)


class PerfectObjectTestCase(BaseTestCase):
    """Test ontic_type.perfect_object method."""

    def test_bad_perfect_usage(self):
        """Ensure handling of bad arguments to perfect)_object method."""
        self.assertRaisesRegexp(
            ValueError,
            r'"the_object" must be provided.',
            o_type.perfect_object, None)

        self.assertRaisesRegexp(
            ValueError,
            r'"the_object" must be OnticType type.',
            o_type.perfect_object, {})

    def test_valid_perfect_usage(self):
        """Ensure that the perfect behavior is correct."""
        schema_def = Schema({
            'prop_1': {'type': 'int'},
            'prop_2': {'type': 'int', 'default': 20},
            'prop_3': {'type': 'int', 'default': 30},
            'prop_4': {'type': 'int', 'default': 40},
        })
        my_type = o_type.create_ontic_type('PerfectOntic', schema_def)

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
        o_type.perfect_object(ontic_object)
        self.assertDictEqual(expected_dict, ontic_object)

    def test_perfect_collection_types(self):
        """Ensure that collection defaults are handled correctly."""
        schema_def = Schema({
            'dict_prop': {
                'type': 'dict',
                'default': {'a': 1, 'b': 2, 'c': 3}
            },
            'list_prop': {
                'type': 'list',
                'default': [1, 2, 3]
            },
            'set_prop': {
                'type': 'set',
                'default': {1, 2, 3}
            }
        })
        my_type = o_type.create_ontic_type('PerfectCollection', schema_def)

        ontic_object = my_type()
        o_type.perfect_object(ontic_object)

        # Test that the collection values are equal
        self.assertDictEqual(schema_def.dict_prop.default,
                             ontic_object.dict_prop)
        self.assertListEqual(schema_def.list_prop.default,
                             ontic_object.list_prop)
        self.assertSetEqual(schema_def.set_prop.default,
                            ontic_object.set_prop)

        # Ensure that the collections are not the same objects
        self.assertIsNot(schema_def.dict_prop.default,
                         ontic_object.dict_prop)
        self.assertIsNot(schema_def.list_prop.default,
                         ontic_object.list_prop)
        self.assertIsNot(schema_def.set_prop.default,
                         ontic_object.set_prop)

    def test_perfect_bad_collection_type(self):
        """Test for the handling of bad collection member o_type."""

    def test_perfect_collection_default_copy(self):
        """Ensure that collection default settings are handled correctly."""
        # Configure default collection.
        default_dict = {'key': 'value'}
        default_list = ['item']
        inner_tuple = (1, 2)
        outer_tuple = (inner_tuple, 3, 4)
        default_set = {'entity', outer_tuple}

        # Configure default collections to test deep copy behavior.
        ontic_object = o_type.OnticType()
        ontic_object.dict = default_dict
        default_deep_dict = {'name': default_dict}
        default_deep_list = [default_dict]
        default_deep_set = {(inner_tuple, outer_tuple)}

        schema_def = Schema({
            'dict_no_default': {
                'type': 'dict',
            },
            'list_no_default': {
                'type': 'list',
            },
            'set_no_default': {
                'type': 'set',
            },
            'dict_with_default': {
                'type': 'dict',
                'default': default_dict,
            },
            'list_with_default': {
                'type': 'list',
                'default': default_list,
            },
            'set_with_default': {
                'type': 'set',
                'default': default_set,
            },
            'dict_deep_default': {
                'type': 'dict',
                'default': default_deep_dict,
            },
            'list_deep_default': {
                'type': 'list',
                'default': default_deep_list,
            },
            'set_deep_default': {
                'type': 'set',
                'default': default_deep_set,
            },
        })

        # Execute test subject.
        my_type = o_type.create_ontic_type('CollectionDefaults', schema_def)
        my_object = my_type()
        o_type.perfect_object(my_object)
        o_type.validate_object(my_object)

        # Assert the no default state.
        self.assertIsNone(my_object.dict_no_default)
        self.assertIsNone(my_object.list_no_default)
        self.assertIsNone(my_object.set_no_default)

        # Assert equality and copy of defaults.
        self.assertDictEqual(default_dict, my_object.dict_with_default)
        self.assertIsNot(default_dict, my_object.dict_with_default)
        self.assertListEqual(default_list, my_object.list_with_default)
        self.assertIsNot(default_list, my_object.list_with_default)
        self.assertSetEqual(default_set, my_object.set_with_default)
        self.assertIsNot(default_set, my_object.set_with_default)

        # Assert equality and copy of deep defaults.
        self.assertDictEqual(default_dict, my_object.dict_deep_default['name'])
        self.assertIsNot(default_deep_dict['name'],
                         my_object.dict_deep_default['name'])
        self.assertDictEqual(default_dict, my_object.list_deep_default[0])
        self.assertIsNot(default_deep_list[0], my_object.list_deep_default[0])
        self.assertSetEqual(default_deep_set, my_object.set_deep_default)
        self.assertIsNot(default_deep_set, my_object.set_deep_default)

    def test_perfect_schema_bad_member_type(self):
        """Test perfect for bad member o_type."""
        invalid_property_schema = OnticProperty(name='invalid_property')
        invalid_property_schema.o_type = list
        invalid_property_schema.member_type = 'UNKNOWN'

        self.maxDiff = None
        self.assertRaisesRegexp(
            ValidationException,
            r"""The value \"UNKNOWN\" for \"member_type\" not in enumeration """
            r"""\[<class 'bool'>, <class 'complex'>, <class 'datetime.date'>"""
            r""", <class 'datetime.datetime'>, <class 'dict'>, """
            r"""<class 'float'>, <class 'int'>, <class 'list'>, <class 'set'>"""
            r""", <class 'str'>, <class 'datetime.time'>, <class 'tuple'>, """
            r"""None\].""",
            property.validate_property, invalid_property_schema)

        value_errors = property.validate_property(
            invalid_property_schema,
            raise_validation_exception=False)
        self.assertEqual(1, len(value_errors))
        self.assertEqual(
            value_errors[0],
            """The value "UNKNOWN" for "member_type" not in enumeration """
            """[<class 'bool'>, <class 'complex'>, <class 'datetime.date'>"""
            """, <class 'datetime.datetime'>, <class 'dict'>, <class 'float'>"""
            """, <class 'int'>, <class 'list'>, <class 'set'>, <class 'str'>"""
            """, <class 'datetime.time'>, <class 'tuple'>, None].""")


class ValidateObjectTestCase(BaseTestCase):
    """Test ontic_types.validate_object method basics."""

    def test_bad_validate_object(self):
        """ValueError testing of validate_object."""
        self.assertRaisesRegexp(
            ValueError,
            'Validation can only support validation of objects derived from '
            'ontic.ontic_type.OnticType.',
            o_type.validate_object, None)
        self.assertRaisesRegexp(
            ValueError,
            'Validation can only support validation of objects derived from '
            'ontic.ontic_type.OnticType.',
            o_type.validate_object, 'Not a OnticType')

    def test_validation_exception_handling(self):
        """Ensure that validate_object handles error reporting."""
        schema_instance = Schema(some_attr={'type': 'int'})
        my_type = o_type.create_ontic_type('ValidateCheck',
                                           schema_instance)
        ontic_object = my_type()
        ontic_object.some_attr = 'WRONG'

        self.assertRaisesRegexp(
            ValidationException,
            r"""The value for "some_attr" is """
            r"""not of type "<class 'int'>": WRONG""",
            o_type.validate_object, ontic_object)

        expected_errors = [
            r"""The value for "some_attr" is not """
            r"""of type "<class 'int'>": WRONG"""]

        try:
            o_type.validate_object(ontic_object)
            self.fail('ValidationException should have been thrown.')
        except ValidationException as ve:
            self.assertListEqual(expected_errors, ve.validation_errors)

        errors = o_type.validate_object(ontic_object,
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
            'ontic_property': {'type': Meta},
            'set_property': {'type': 'set'},
            'str_property': {'type': 'str'},
            'date_property': {'type': 'date'},
            'time_property': {'type': 'time'},
            'datetime_property': {'type': 'datetime'},
        }

        # Create the o_type
        my_type = o_type.create_ontic_type('TypeCheck', schema)
        self.assertIsNotNone(o_type)

        # Create object of o_type
        ontic_object = my_type()

        # Validate an empty object.
        o_type.validate_object(ontic_object)

        # Validate with known good data.
        ontic_object.bool_property = True
        ontic_object.dict_property = {'some_key': 'some_value'}
        ontic_object.core_type_property = Meta({'key': 'val'})
        ontic_object.float_property = 3.4
        ontic_object.int_property = 5
        ontic_object.list_property = [5, 6, 7]
        ontic_object.set_property = {'dog', 'cat', 'mouse'}
        ontic_object.str_property = 'some_string'
        ontic_object.date_property = date(2000, 1, 1)
        ontic_object.time_property = time(12, 30, 30)
        ontic_object.datetime_property = datetime(2001, 1, 1, 12, 30, 30)
        o_type.validate_object(ontic_object)

        # Validate with known bad data.
        ontic_object.bool_property = 'Dog'
        self.assertRaisesRegexp(
            ValidationException,
            r"""The value for "bool_property" is not """
            r"""of type "<class 'bool'>": Dog""",
            o_type.validate_object, ontic_object)
        ontic_object.bool_property = True

        # Validate a string vs a list o_type
        ontic_object.list_property = 'some_string'
        self.assertRaisesRegexp(
            ValidationException,
            r"""The value for "list_property" is not """
            r"""of type "<class 'list'>": some_string""",
            o_type.validate_object, ontic_object)

    def test_type_bad_setting(self):
        """ValueError for bad 'type' setting."""
        schema = {
            'some_property': {'type': 'Unknown'}
        }

        self.assertRaisesRegexp(
            ValueError,
            r"""Illegal type declaration: Unknown""",
            o_type.create_ontic_type, 'Dummy', schema)

    def test_required_setting(self):
        """Validate 'required' schema setting."""
        schema = {
            'some_property': {'required': True},
            'other_property': {'required': False}
        }

        # Create the o_type
        my_type = o_type.create_ontic_type('RequireCheck', schema)
        self.assertIsNotNone(o_type)

        # Create object of o_type
        ontic_object = my_type()

        # Validate an empty object, which should cause ValueError
        self.assertRaisesRegexp(
            ValidationException,
            'The value for "some_property" is required.',
            o_type.validate_object, ontic_object)

        # Validate with data
        ontic_object.some_property = 'Something'
        ontic_object.other_property = 'Other'
        o_type.validate_object(ontic_object)

    def test_enum_setting(self):
        """Validate 'enum' schema setting."""
        # Scalar testing
        # ###############
        schema = {
            'enum_property': {'enum': {'some_value', 99}}
        }

        # Create the o_type
        my_type = o_type.create_ontic_type('EnumCheck', schema)
        self.assertIsNotNone(my_type)

        # Create object of o_type
        ontic_object = my_type()

        # Validate an empty object
        o_type.validate_object(ontic_object)

        # Validate a good setting
        ontic_object.enum_property = 99
        o_type.validate_object(ontic_object)

        # Validate a bad setting
        ontic_object.enum_property = 'bad, bad, bad'
        self.assertRaisesRegexp(
            ValidationException,
            r"""The value "bad, bad, bad" for "enum_property" not in """
            r"""enumeration (\['some_value', 99\]|\[99, 'some_value'\])\.""",
            o_type.validate_object, ontic_object)

    def test_collection_enum_setting(self):
        """Validate 'enum' schema setting on collections."""
        schema = {
            'enum_property': {'type': 'list', 'enum': {'dog', 'cat'}}
        }

        # Create the o_type
        my_type = o_type.create_ontic_type('EnumListCheck', schema)
        self.assertIsNotNone(o_type)

        # Create object of o_type
        ontic_object = my_type()

        # Validate an empty object, as required not set.
        o_type.validate_object(ontic_object)

        # Validate a good setting
        ontic_object.enum_property = ['dog']
        o_type.validate_object(ontic_object)

        # Validate a bad setting
        ontic_object.enum_property = ['fish']
        self.assertRaisesRegexp(
            ValidationException,
            r'''The value "fish" for "enum_property" not in'''
            r''' enumeration \['cat', 'dog'\].''',
            o_type.validate_object, ontic_object)

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

        my_type = o_type.create_ontic_type('MinCheck', schema)
        self.assertIsNotNone(o_type)

        ontic_object = my_type()

        # None test, with no required fields
        o_type.validate_object(ontic_object)

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
        o_type.validate_object(ontic_object)

        # Str failure
        ontic_object.str_min_property = '1'
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "1" for "str_min_property" '
            'fails min of 5.',
            o_type.validate_object, ontic_object)
        ontic_object.str_min_property = '8 letters'

        # Int failure
        ontic_object.int_min_property = 5
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "5" for "int_min_property" '
            'fails min of 10.',
            o_type.validate_object, ontic_object)
        ontic_object.int_min_property = 20

        # Float failure
        ontic_object.float_min_property = 15.0
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "15.0" for "float_min_property" '
            'fails min of 20.',
            o_type.validate_object, ontic_object)
        ontic_object.float_min_property = 30.0

        # List failure
        ontic_object.list_min_property = list()
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "\[]" for "list_min_property" '
            'fails min of 1.',
            o_type.validate_object, ontic_object)
        ontic_object.list_min_property = ['one item']

        # Set failure
        ontic_object.set_min_property = set()
        self.assertRaisesRegexp(
            ValidationException,
            r"""The value of \"set\(\)\" """
            r"""for "set_min_property" fails min of 1.""",
            o_type.validate_object, ontic_object)
        ontic_object.set_min_property = {'one item'}

        # Dict failure
        ontic_object.dict_min_property = dict()
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "{}" for "dict_min_property" '
            'fails min of 1.',
            o_type.validate_object, ontic_object)
        ontic_object.dict_min_property = {'some_key': 'one_item'}

        # Date failure
        ontic_object.date_min_property = date(1999, 1, 1)
        self.assertRaisesRegexp(
            ValidationException,
            'date_min_property" fails min of 2000-01-01.',
            o_type.validate_object, ontic_object)
        ontic_object.date_min_property = date(2001, 1, 1)

        # Time failure
        ontic_object.time_min_property = time(11, 30, 30)
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "11:30:30" for "time_min_property" '
            'fails min of 12:30:30.',
            o_type.validate_object, ontic_object)
        ontic_object.time_min_property = time(13, 30, 30)

        # Datetime failure
        ontic_object.datetime_min_property = datetime(1999, 1, 1, 11, 30, 30)
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "1999-01-01 11:30:30" for "datetime_min_property" '
            'fails min of 2000-01-01 12:30:30.',
            o_type.validate_object, ontic_object)

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

        my_type = o_type.create_ontic_type('MaxCheck', schema)
        self.assertIsNotNone(o_type)

        ontic_object = my_type()

        # None test, with no required fields
        o_type.validate_object(ontic_object)

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
        o_type.validate_object(ontic_object)

        # Str failure
        ontic_object.str_max_property = '8 letters'
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "8 letters" for '
            '"str_max_property" fails max of 5.',
            o_type.validate_object, ontic_object)
        ontic_object.str_max_property = 'small'

        # Int failure
        ontic_object.int_max_property = 20
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "20" for "int_max_property" '
            'fails max of 10.',
            o_type.validate_object, ontic_object)
        ontic_object.int_max_property = 5

        # Float failure
        ontic_object.float_max_property = 30.0
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "30.0" for "float_max_property" fails max of 20.',
            o_type.validate_object, ontic_object)
        ontic_object.float_max_property = 15.0

        # List failure
        ontic_object.list_max_property = ['one item', 'two item']
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "\[\'one item\', \'two item\'\]" '
            'for "list_max_property" fails max of 1.',
            o_type.validate_object, ontic_object)
        ontic_object.list_max_property = ['one item']

        # Set failure
        ontic_object.set_max_property = {'one item', 'two item'}
        expected_error = (
            r"""The value of """
            r"""("\{'two item', 'one item'\}"|"\{'one item', 'two item'\}") """
            r"""for "set_max_property" fails max of 1\.""")

        self.assertRaisesRegexp(
            ValidationException,
            expected_error,
            o_type.validate_object, ontic_object)
        ontic_object.set_max_property = {'one item'}

        # Dict failure
        ontic_object.dict_max_property = {'some_key': 'one_item',
                                          'another_key': 'two_item'}
        self.assertRaisesRegexp(
            ValidationException,
            r"""The value of """
            r"""("{'some_key': 'one_item', 'another_key': 'two_item'}"|"""
            r""""{'another_key': 'two_item', 'some_key': 'one_item'}")"""
            r""" for "dict_max_property" fails max of 1.""",
            o_type.validate_object, ontic_object)
        ontic_object.dict_max_property = {'some_key': 'one_item'}

        # Date failure
        ontic_object.date_max_property = date(2001, 1, 1)
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "2001-01-01" for '
            '"date_max_property" fails max of 2000-01-01.',
            o_type.validate_object, ontic_object)
        ontic_object.date_max_property = date(2001, 1, 1)

        # Time failure
        ontic_object.time_max_property = time(13, 30, 30)
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "13:30:30" for "time_max_property" '
            'fails max of 12:30:30.',
            o_type.validate_object, ontic_object)
        ontic_object.time_max_property = time(13, 30, 30)

        # Datetime failure
        ontic_object.datetime_max_property = datetime(2001, 1, 1, 11, 30, 30)
        self.assertRaisesRegexp(
            ValidationException,
            'The value of "2001-01-01 11:30:30" for "datetime_max_property" '
            'fails max of 2000-01-01 12:30:30.',
            o_type.validate_object, ontic_object)

    def test_regex_setting(self):
        """Validate 'regex' schema setting."""
        schema = {
            'b_only_property': {'type': 'str', 'regex': '^b+'}
        }

        my_type = o_type.create_ontic_type('RegexCheck', schema)
        self.assertIsNotNone(o_type)

        ontic_object = my_type()

        # None test, with no required fields
        o_type.validate_object(ontic_object)

        # Good test
        ontic_object.b_only_property = ''
        o_type.validate_object(ontic_object)
        ontic_object.b_only_property = 'b'
        o_type.validate_object(ontic_object)

        # Bad test
        ontic_object.b_only_property = 'a'
        self.assertRaisesRegexp(
            ValidationException,
            'Value \"a\" for b_only_property does not '
            'meet regex: \^b\+',
            o_type.validate_object, ontic_object)

    def test_member_type_setting(self):
        """Validate 'member_type' setting."""
        schema = {
            'list_property': {'type': 'list', 'member_type': 'str'}
        }

        my_type = o_type.create_ontic_type('ItemTypeCheck', schema)
        self.assertIsNotNone(o_type)

        ontic_object = my_type()

        # None test, with no required fields.
        o_type.validate_object(ontic_object)

        # Good test
        ontic_object.list_property = []
        o_type.validate_object(ontic_object)
        ontic_object.list_property.append('some_item')
        o_type.validate_object(ontic_object)

        # Bad test
        ontic_object.list_property.append(99)
        self.assertRaisesRegexp(
            ValidationException,
            r'''The value "99" for "list_property" is not of type '''
            r'''"<class 'str'>".''',
            o_type.validate_object, ontic_object)

    def test_collection_regex_setting(self):
        """Validate string collection with 'regex' setting."""
        schema = {
            'set_property': {'type': set, 'member_type': str, 'regex': 'b+'}
        }

        my_type = o_type.create_ontic_type(
            'CollectionRegexCheck', schema)
        self.assertIsNotNone(o_type)

        ontic_object = my_type()

        # None test, with no required fields.
        o_type.validate_object(ontic_object)

        # Good test
        ontic_object.set_property = set()
        o_type.validate_object(ontic_object)
        ontic_object.set_property.add('bbbbb')
        o_type.validate_object(ontic_object)

        # Bad test
        ontic_object.set_property.add('xxxxxx')
        self.assertRaisesRegexp(
            ValidationException,
            r'''Value "xxxxxx" for "set_property" does not meet regex: b+''',
            o_type.validate_object, ontic_object)

    def test_member_min_setting(self):
        """Validate 'member_min' setting."""
        # Test the item min setting for string items.
        schema = {
            'list_property': {'type': 'list', 'member_type': 'str',
                              'member_min': 4}
        }

        my_type = o_type.create_ontic_type('StrItemMinCheck', schema)
        self.assertIsNotNone(o_type)

        ontic_object = my_type()

        # None test, with no required fields.
        o_type.validate_object(ontic_object)

        # Good Test
        ontic_object.list_property = []
        o_type.validate_object(ontic_object)
        ontic_object.list_property.append('four')
        o_type.validate_object(ontic_object)

        # Bad Test
        ontic_object.list_property.append('one')
        self.assertRaisesRegexp(
            ValidationException,
            r'''The value of "one" for "list_property" '''
            r'''fails min length of 4.''',
            o_type.validate_object, ontic_object)

        # Test the item min setting for numeric items.
        schema = {
            'list_property': {'type': 'list', 'member_type': 'int',
                              'member_min': 4}
        }

        my_type = o_type.create_ontic_type('StrItemMinCheck', schema)
        self.assertIsNotNone(o_type)

        ontic_object = my_type()

        # None test, with no required fields.
        o_type.validate_object(ontic_object)

        # Good Test
        ontic_object.list_property = []
        o_type.validate_object(ontic_object)
        ontic_object.list_property.append(4)
        o_type.validate_object(ontic_object)

        # Bad Test
        ontic_object.list_property.append(1)
        self.assertRaisesRegexp(
            ValidationException,
            r'''The value of "1" for "list_property" fails min size of 4.''',
            o_type.validate_object, ontic_object)

    def test_member_max_setting(self):
        """Validate 'member_max' setting."""
        # Test the item max setting for string items.
        schema = {
            'list_property': {
                'type': 'list', 'member_type': 'str', 'member_max': 4}
        }

        my_type = o_type.create_ontic_type('StrItemMinCheck', schema)
        self.assertIsNotNone(my_type)

        ontic_object = my_type()

        # None test, with no required fields.
        o_type.validate_object(ontic_object)

        # Good Test
        ontic_object.list_property = []
        o_type.validate_object(ontic_object)
        ontic_object.list_property.append('four')
        o_type.validate_object(ontic_object)

        # Bad Test
        ontic_object.list_property.append('seven')
        self.assertRaisesRegexp(
            ValidationException,
            r'''The value of "seven" for "list_property" '''
            r'''fails max length of 4.''',
            o_type.validate_object, ontic_object)

        # Test the item min setting for numeric items.
        schema = {
            'list_property': {
                'type': 'list', 'member_type': 'int', 'member_max': 4}
        }

        my_type = o_type.create_ontic_type('StrItemMinCheck', schema)
        self.assertIsNotNone(o_type)

        ontic_object = my_type()

        # None test, with no required fields.
        o_type.validate_object(ontic_object)

        # Good Test
        ontic_object.list_property = []
        o_type.validate_object(ontic_object)
        ontic_object.list_property.append(4)
        o_type.validate_object(ontic_object)

        # Bad Test
        ontic_object.list_property.append(7)
        self.assertRaisesRegexp(
            ValidationException,
            r'''The value of "7" for "list_property" fails max size of 4.''',
            o_type.validate_object, ontic_object)


class ValidateValueTestCase(BaseTestCase):
    """Test ontic_types.validate_value method."""

    def test_bad_validate_value(self):
        """ValueError testing of validate_value."""
        self.assertRaisesRegexp(
            ValueError,
            '"ontic_object" is required, cannot be None.',
            o_type.validate_value, 'some_value', None)

        self.assertRaisesRegexp(
            ValueError,
            '"ontic_object" must be OnticType or child type of OnticType',
            o_type.validate_value, 'some_value', "can't be string")

        my_type = o_type.create_ontic_type(
            'BadValidateValue',
            {
                'prop1': {'type': 'int'}
            })
        ontic_object = my_type()
        ontic_object.prop1 = 1

        self.assertRaisesRegexp(
            ValueError,
            '"property_name" is required, cannot be None.',
            o_type.validate_value, None, ontic_object)

        self.assertRaisesRegexp(
            ValueError,
            r'"property_name" is not a valid string.',
            o_type.validate_value, '', ontic_object)

        self.assertRaisesRegexp(
            ValueError,
            '"property_name" is not a valid string.',
            o_type.validate_value, 5, ontic_object)

        self.assertRaisesRegexp(
            ValueError,
            '"illegal property name" is not a recognized property.',
            o_type.validate_value, 'illegal property name', ontic_object)

    def test_validate_value_exception_handling(self):
        """Ensure validation exception handling by validation_object method."""
        schema_instance = Schema(some_attr={'type': 'int'})
        my_type = o_type.create_ontic_type('ValidateCheck',
                                           schema_instance)
        ontic_object = my_type()
        ontic_object.some_attr = 'WRONG'

        self.assertRaisesRegexp(
            ValidationException,
            r"""The value for "some_attr" is not of type "<class 'int'>":"""
            r""" WRONG""",
            o_type.validate_value, 'some_attr', ontic_object)

        with self.assertRaises(ValidationException) as ve:
            o_type.validate_value('some_attr', ontic_object)
        expected_errors = [
            r"""The value for "some_attr" is not """
            r"""of type "<class 'int'>": WRONG"""
        ]
        self.assertListEqual(expected_errors, ve.exception.validation_errors)

        errors = o_type.validate_value('some_attr', ontic_object,
                                       raise_validation_exception=False)
        self.assertListEqual(expected_errors, errors)

    def test_validate_value_value_arg(self):
        """Valid value argument testing of validate_value."""
        # Test that scalar property is valid.
        single_property_schema = {
            'prop1': {'type': 'str'}
        }
        my_type = o_type.create_ontic_type(
            'GoodValidateValue', single_property_schema)
        ontic_object = my_type({'prop1': 'Hot Dog'})
        o_type.validate_value('prop1', ontic_object)


class ChildOnticType(OnticType):
    ONTIC_SCHEMA = Schema([
        OnticProperty(name='int_prop',
                      type=int),
        OnticProperty(name='str_prop',
                      type=str,
                      required=True,
                      default='A Value')
    ])


class ParentOnticType(OnticType):
    ONTIC_SCHEMA = Schema([
        OnticProperty(name='child_prop', type=ChildOnticType)
    ])


DEFAULT_CHILD_PROP = ChildOnticType(int_prop=99, str_prop='The Value')


class RequiredOnticChildType(OnticType):
    ONTIC_SCHEMA = Schema([
        OnticProperty(
            name='child_prop',
            type=ChildOnticType,
            required=True,
            default=DEFAULT_CHILD_PROP),
    ])


class SettingOnticTypeTestCase(BaseTestCase):
    """Test case the setting of an OnticType as a OnticProperty.type setting."""

    def test_ontic_type_perfect(self):
        """Test that Ontic child properties are perfected with parent."""
        parent = ParentOnticType()
        parent.child_prop = ChildOnticType()

        self.assertNotIn('int_prop', parent.child_prop)
        self.assertNotIn('str_prop', parent.child_prop)
        parent.perfect()
        self.assertIsNone(parent.child_prop.int_prop)
        self.assertEqual('A Value', parent.child_prop.str_prop)

        res = parent.validate()
        self.assertListEqual([], res)

    def test_ontic_type_success(self):
        """Test validation of an OnticType property."""
        parent = ParentOnticType()
        parent.child_prop = ChildOnticType(str_prop='Some Value')
        parent.child_prop.int_prop = 1

        res = parent.validate(raise_validation_exception=True)
        self.assertListEqual(res, [])

    def test_non_ontic_type_failure(self):
        """Test validation of an incorrect OnticType property."""
        parent = ParentOnticType()
        parent.child_prop = ChildOnticType()
        parent.child_prop.int_prop = '1'

        self.assertRaisesRegexp(
            ValidationException,
            r"""The child property child_prop, has errors:: """
            r"""The value for "int_prop" is not of o_type "<class 'int'>": 1"""
            r""" || The value for "str_prop" is required.""",
            parent.validate,
            raise_validation_exception=True)

    def test_ontic_type_default_setting(self):
        """Ensure that an OnticType property default is copied upon perfect."""
        parent = RequiredOnticChildType()

        self.assertNotIn('child_prop', parent)

        parent.perfect()

        self.assertIn('child_prop', parent)
        self.assertIsNot(DEFAULT_CHILD_PROP, parent.child_prop)
        self.assertEqual(99, parent.child_prop.int_prop)
        self.assertEqual('The Value', parent.child_prop.str_prop)

        self.assertEqual([], parent.validate())
