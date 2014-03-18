"""Testing suite for object_tools module."""
import base_test_case

from ook import object_tools
from ook.object_type import BaseType, PropertySchema, SchemaType


class CreateOokTypeTestCase(base_test_case.BaseTestCase):
    """Test the dynamic creation of Ook types."""

    def test_create_ook_type_arg_errors(self):
        """Assert the create ook type arg errors."""
        self.assertRaisesRegexp(
            ValueError, 'The string "name" argument is required.',
            object_tools.create_ook_type, name=None, schema=dict())
        self.assertRaisesRegexp(
            ValueError, 'The schema dictionary is required.',
            object_tools.create_ook_type, name='SomeName', schema=None)
        self.assertRaisesRegexp(
            ValueError, 'The schema must be a dict.',
            object_tools.create_ook_type, name='SomeName', schema=list())

    def test_create_ook_type(self):
        """The most simple and basic dynamic Ook."""
        ook_type = object_tools.create_ook_type('Simple', dict())

        self.assertIsNotNone(ook_type)

        ook_object = ook_type()
        self.assert_dynamic_accessing(ook_object)
        self.assertIsInstance(ook_object, ook_type)


class ValidateObjectTestCase(base_test_case.BaseTestCase):
    """Test object_tools.validate_object method basics."""

    def test_bad_validate_object(self):
        """ValueError testing of validate_object."""
        self.assertRaisesRegexp(
            ValueError,
            'Validation can only support validation of objects derived from ook.BaseType.',
            object_tools.validate_object, None)
        self.assertRaisesRegexp(
            ValueError,
            'Validation can only support validation of objects derived from ook.BaseType.',
            object_tools.validate_object, 'Not a BaseType')

    def test_type_setting(self):
        """Validate 'type' schema setting."""
        schema = {
            'bool_property': {'type': 'bool'},
            'dict_property': {'type': 'dict'},
            'float_property': {'type': 'float'},
            'int_property': {'type': 'int'},
            'list_property': {'type': 'list'},
            'set_property': {'type': 'set'},
            'str_property': {'type': 'str'}
        }

        # Create the type
        ook_type = object_tools.create_ook_type('TypeCheck', schema)
        self.assertIsNotNone(ook_type)
        object_tools.validate_schema(ook_type.get_schema())

        # Create object of type
        ook_object = ook_type()

        # Validate an empty object.
        object_tools.validate_object(ook_object)

        # Validate with known good data.
        ook_object.bool_property = True
        ook_object.dict_property = {'some_key': 'some_value'}
        ook_object.float_property = 3.4
        ook_object.int_property = 5
        ook_object.list_property = [5, 6, 7]
        ook_object.set_property = {'dog', 'cat', 'mouse'}
        ook_object.str_property = 'some_string'
        object_tools.validate_object(ook_object)

        # Validate with known bad data.
        ook_object.bool_property = 'Dog'
        self.assertRaisesRegexp(
            ValueError,
            'The value for "bool_property" is not of type "bool": Dog',
            object_tools.validate_object, ook_object)

    def test_type_bad_setting(self):
        """ValueError for bad 'type' setting."""
        schema = {
            'some_property': {'type': 'Unknown'}
        }
        # Create the type
        self.assertRaisesRegexp(
            ValueError,
            "The value \"Unknown\" for \"type\" not in enumeration "
            "\['set', 'int', 'float', 'list', 'dict', 'str', 'bool'\].",
            object_tools.create_ook_type, 'Dummy', schema)

    def test_required_setting(self):
        """Validate 'required' schema setting."""
        schema = {
            'some_property': {'required': True}
        }

        # Create the type
        ook_type = object_tools.create_ook_type('RequireCheck', schema)
        self.assertIsNotNone(ook_type)
        object_tools.validate_schema(ook_type.get_schema())

        # Create object of type
        ook_object = ook_type()

        # Validate an empty object, which should cause ValueError
        self.assertRaisesRegexp(
            ValueError, 'The value for "some_property" is required.',
            object_tools.validate_object, ook_object)

        # Validate with data
        ook_object.some_property = 'Something'

    def test_enum_setting(self):
        """Validate 'enum' schema setting."""
        schema = {
            'enum_property': {'enum': {'some_value', 99}}
        }

        # Create the type
        ook_type = object_tools.create_ook_type('EnumCheck', schema)
        self.assertIsNotNone(ook_type)
        object_tools.validate_schema(ook_type.get_schema())

        # Create object of type
        ook_object = ook_type()

        # Validate an empty object
        object_tools.validate_object(ook_object)

        # Validate a good setting
        ook_object.enum_property = 99
        object_tools.validate_object(ook_object)

        # Validate a bad setting
        ook_object.enum_property = 'bad, bad, bad'
        self.assertRaisesRegexp(
            ValueError,
            "The value \"bad, bad, bad\" for \"enum_property\" "
            "not in enumeration \[99, 'some_value'\].",
            object_tools.validate_object, ook_object)

    def test_min_setting(self):
        """Validate 'min' schema setting."""
        schema = {
            'str_min_property': {'type': 'str', 'min': 5},
            'int_min_property': {'type': 'int', 'min': 10},
            'float_min_property': {'type': 'float', 'min': 20},
            'list_min_property': {'type': 'list', 'min': 1},
            'set_min_property': {'type': 'set', 'min': 1},
            'dict_min_property': {'type': 'dict', 'min': 1},
        }

        ook_type = object_tools.create_ook_type('MinCheck', schema)
        self.assertIsNotNone(ook_type)
        object_tools.validate_schema(ook_type.get_schema())

        ook_object = ook_type()

        # None test, with no required fields
        object_tools.validate_object(ook_object)

        # Good test
        ook_object.str_min_property = '8 letters'
        ook_object.int_min_property = 20
        ook_object.float_min_property = 30.0
        ook_object.list_min_property = ['one item']
        ook_object.set_min_property = {'one item'}
        ook_object.dict_min_property = {'some_kee': 'one item'}
        object_tools.validate_object(ook_object)

        # Str failure
        ook_object.str_min_property = '1'
        self.assertRaisesRegexp(ValueError,
                                'The value of "1" for "str_min_property" fails min of 5.',
                                object_tools.validate_object, ook_object)
        ook_object.str_min_property = '8 letters'

        # Int failure
        ook_object.int_min_property = 5
        self.assertRaisesRegexp(ValueError,
                                'The value of "5" for "int_min_property" fails min of 10.',
                                object_tools.validate_object, ook_object)
        ook_object.int_min_property = 20

        # Float failure
        ook_object.float_min_property = 15.0
        self.assertRaisesRegexp(ValueError,
                                'The value of "15.0" for "float_min_property" fails min of 20.',
                                object_tools.validate_object, ook_object)
        ook_object.float_min_property = 30.0

        # List failure
        ook_object.list_min_property = list()
        self.assertRaisesRegexp(ValueError,
                                'The value of "\[]" for "list_min_property" fails min of 1.',
                                object_tools.validate_object, ook_object)
        ook_object.list_min_property = ['one item']

        # Set failure
        ook_object.set_min_property = set()
        self.assertRaisesRegexp(ValueError,
                                'The value of "set\(\[]\)" for "set_min_property" fails min of 1.',
                                object_tools.validate_object, ook_object)
        ook_object.set_min_property = {'one item'}

        # Dict failure
        ook_object.dict_min_property = dict()
        self.assertRaisesRegexp(ValueError,
                                'The value of "{}" for "dict_min_property" fails min of 1.',
                                object_tools.validate_object, ook_object)
        ook_object.dict_min_property = {'some_key': 'one_item'}

    def test_max_setting(self):
        """Validate 'max' schema setting."""
        schema = {
            'str_max_property': {'type': 'str', 'max': 5},
            'int_max_property': {'type': 'int', 'max': 10},
            'float_max_property': {'type': 'float', 'max': 20},
            'list_max_property': {'type': 'list', 'max': 1},
            'set_max_property': {'type': 'set', 'max': 1},
            'dict_max_property': {'type': 'dict', 'max': 1},
        }

        ook_type = object_tools.create_ook_type('MaxCheck', schema)
        self.assertIsNotNone(ook_type)
        #object_tools.validate_schema(ook_type.get_schema())

        ook_object = ook_type()

        # None test, with no required fields
        object_tools.validate_object(ook_object)

        # Good test
        ook_object.str_max_property = 'small'
        ook_object.int_max_property = 5
        ook_object.float_max_property = 10.0
        ook_object.list_max_property = ['one item']
        ook_object.set_max_property = {'one item'}
        ook_object.dict_max_property = {'some_kee': 'one item'}
        object_tools.validate_object(ook_object)

        # Str failure
        ook_object.str_max_property = '8 letters'
        self.assertRaisesRegexp(ValueError,
                                'The value of "8 letters" for "str_max_property" fails max of 5.',
                                object_tools.validate_object, ook_object)
        ook_object.str_max_property = 'small'

        # Int failure
        ook_object.int_max_property = 20
        self.assertRaisesRegexp(ValueError,
                                'The value of "20" for "int_max_property" fails max of 10.',
                                object_tools.validate_object, ook_object)
        ook_object.int_max_property = 5

        # Float failure
        ook_object.float_max_property = 30.0
        self.assertRaisesRegexp(
            ValueError,
            'The value of "30.0" for "float_max_property" fails max of 20.',
            object_tools.validate_object, ook_object)
        ook_object.float_max_property = 15.0

        # List failure
        ook_object.list_max_property = ['one item', 'two item']
        self.assertRaisesRegexp(
            ValueError,
            'The value of "\[\'one item\', \'two item\'\]" '
            'for "list_max_property" fails max of 1.',
            object_tools.validate_object, ook_object)
        ook_object.list_max_property = ['one item']

        # Set failure
        ook_object.set_max_property = {'one item', 'two item'}
        self.assertRaisesRegexp(
            ValueError,
            'The value of "set\(\[\'one item\', \'two item\'\]\)" '
            'for "set_max_property" fails max of 1.',
            object_tools.validate_object, ook_object)
        ook_object.set_max_property = {'one item'}

        # Dict failure
        ook_object.dict_max_property = {'some_key': 'one_item', 'another_key': 'two_item'}
        self.assertRaisesRegexp(
            ValueError,
            'The value of "{\'another_key\': \'two_item\', \'some_key\': \'one_item\'}" for '
            '"dict_max_property" fails max of 1.',
            object_tools.validate_object, ook_object)
        ook_object.dict_max_property = {'some_key': 'one_item'}

    def test_regex_setting(self):
        """Validate 'regex' schema setting."""
        schema = {
            'b_only_property': {'type': 'str', 'regex': '^b+'}
        }

        ook_type = object_tools.create_ook_type('RegexCheck', schema)
        self.assertIsNotNone(ook_type)
        object_tools.validate_schema(ook_type.get_schema())

        ook_object = ook_type()

        # None test, with no required fields
        object_tools.validate_object(ook_object)

        # Good test
        ook_object.b_only_property = 'b'
        object_tools.validate_object(ook_object)

        # Bad test
        ook_object.b_only_property = 'a'
        self.assertRaisesRegexp(ValueError,
                                'Value \"a\" for b_only_property does not meet regex: \^b\+',
                                object_tools.validate_object, ook_object)


class ValidateValueTestCase(base_test_case.BaseTestCase):
    """Test object_tools.validate_value method."""

    def test_bad_validate_value(self):
        """ValueError testing of validate_value."""
        self.assertRaisesRegexp(
            ValueError,
            '"property_schema" is not provided.',
            object_tools.validate_value, 'some_value', None)

        self.assertRaisesRegexp(
            ValueError,
            '"property_schema" is not of type dict, BaseType, or PropertySchema',
            object_tools.validate_value, 'some_value', "can't be string")

        self.assertRaisesRegexp(
            ValueError,
            'The value for "value" is not of type "int": some_value',
            object_tools.validate_value, 'some_value', {'type': 'int'})


    def test_validate_value_schema_arg(self):
        """Valid property_schema argument testing of validate_value."""
        # Tests that dict type is a valid argument.
        test_property_schema = {'type': 'str', 'required': True}
        object_tools.validate_value("some value", test_property_schema)

        # Test that BaseType is a valid argument.
        test_base_type = BaseType(test_property_schema)
        object_tools.validate_value('some_value', test_base_type)

        # Test that PropertySchema is a valud argument.
        test_property_schema = PropertySchema(test_property_schema)
        object_tools.validate_value('some_value', test_property_schema)

    def test_validate_value_value_arg(self):
        """Valid value argument testing of validate_value."""
        # Test that scalar property is valid.
        single_property_schema = PropertySchema({
            'type': 'str'
        })
        object_tools.validate_value('Hot Dog', single_property_schema)

        self.assertRaisesRegexp(
            ValueError,
            'The value for "value" is not of type "str": 4',
            object_tools.validate_value, 4, single_property_schema)

        collection_property_schema = PropertySchema({
            'type': 'list',
            'item_type': 'str',
        })
        collection_value = ['Hot Dog', 'Hamburger']
        object_tools.validate_value(collection_value, collection_property_schema)

        collection_value.append(4)
        self.assertRaisesRegexp(
            ValueError,
            'blah',
            object_tools.validate_value, collection_value, collection_property_schema)


class ValidateSchemaTestCase(base_test_case.BaseTestCase):
    """Test object_tools.validate_schema method."""

    def test_bad_validate_schema(self):
        """ValueError testing of validate_schema."""
        self.assertRaisesRegexp(
            ValueError,
            '"property_schema" argument must be of type dict, BaseType, or SchemaType.',
            object_tools.validate_schema, None)
        self.assertRaisesRegexp(
            ValueError,
            '"property_schema" argument must be of type dict, BaseType, or SchemaType.',
            object_tools.validate_schema, "not a schema")

    def test_validate_schema(self):
        """Valid schema testing of validate_schema."""
        schema = {'some_attribute': {'type': 'int'}}

        # Dict test
        object_tools.validate_schema(schema)

        # BaseType test
        base_type_schema = BaseType(schema)
        object_tools.validate_schema(base_type_schema)

        # SchemaType test
        schema_type_schema = SchemaType(schema)
        object_tools.validate_schema(schema_type_schema)
