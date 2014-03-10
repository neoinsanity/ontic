import base_test_case

from ook import object_tools
from ook.object_type import BaseType, SchemaType


class CreateOokTypeTest(base_test_case.BaseTestCase):
    """Test the dynamic creation of Ook types."""

    def test_create_ook_type_arg_errors(self):
        """Assert the create ook type arg errors."""
        self.assertRaises(
            ValueError, object_tools.create_ook_type, name=None, schema=dict())
        self.assertRaises(
            ValueError, object_tools.create_ook_type, name='SomeName', schema=None)
        self.assertRaises(
            ValueError, object_tools.create_ook_type, name='SomeName', schema=list())

    def test_create_ook_type(self):
        """The most simple and basic dynamic Ook."""
        ook_type = object_tools.create_ook_type('Barebone', dict())

        self.assertIsNotNone(ook_type)

        ook_object = ook_type()
        self.assert_dynamic_accessing(ook_object)
        self.assertIsInstance(ook_object, ook_type)


class ValidateSchemaTestCase(base_test_case.BaseTestCase):
    def test_bad_validate_schema(self):
        self.assertRaises(ValueError, object_tools.validate_schema, None)
        self.assertRaises(ValueError, object_tools.validate_schema, "not a schema")

    def test_validate_schema(self):
        schema = {'some_attribute': {'type': 'int'}}

        # Dict test
        object_tools.validate_schema(schema)

        # BaseType test
        base_type_schema = BaseType(schema)
        object_tools.validate_schema(base_type_schema)

        # SchemaType test
        schema_type_schea = SchemaType(schema)
        object_tools.validate_schema(schema_type_schea)


class ValidateObjectTestCase(base_test_case.BaseTestCase):
    def test_bad_validate_object(self):
        self.assertRaises(ValueError, object_tools.validate_object, None)
        self.assertRaises(ValueError, object_tools.validate_object, 'Not a BaseType')


class PropertySchemaTest(base_test_case.BaseTestCase):
    def test_type_setting(self):
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
        ook_type = object_tools.create_ook_type('Typer', schema)
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
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)

    def test_type_bad_setting(self):
        schema = {
            'some_property': {'type': 'Unknown'}
        }
        # Create the type
        ook_type = object_tools.create_ook_type('Dummy', schema)

    def test_required_setting(self):
        schema = {
            'some_property': {'required': True}
        }

        # Create the type
        ook_type = object_tools.create_ook_type('Requirer', schema)
        self.assertIsNotNone(ook_type)
        object_tools.validate_schema(ook_type.get_schema())

        # Create object of type
        ook_object = ook_type()

        # Validate an empty object, which should cause ValueError
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)

        # Validate with data
        ook_object.some_property = 'Something'


    def test_enum_setting(self):
        schema = {
            'enum_property': {'enum': {'some_value', 99}}
        }

        # Create the type
        ook_type = object_tools.create_ook_type('Enumer', schema)
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
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)

    def test_min_setting(self):
        schema = {
            'str_min_property': {'type': 'str', 'min': 5},
            'int_min_property': {'type': 'int', 'min': 10},
            'float_min_property': {'type': 'float', 'min': 20},
            'list_min_property': {'type': 'list', 'min': 1},
            'set_min_property': {'type': 'set', 'min': 1},
            'dict_min_property': {'type': 'dict', 'min': 1},
        }

        ook_type = object_tools.create_ook_type('Miner', schema)
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
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)
        ook_object.str_min_property = '8 letters'

        # Int failure
        ook_object.int_min_property = 5
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)
        ook_object.int_min_property = 20

        # Float failure
        ook_object.float_min_property = 15.0
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)
        ook_object.float_min_property = 30.0

        # List failure
        ook_object.list_min_property = list()
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)
        ook_object.list_min_property = ['one item']

        # Set failure
        ook_object.set_min_property = set()
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)
        ook_object.set_min_property = {'one item'}

        # Dict failure
        ook_object.dict_min_property = dict()
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)
        ook_object.dict_min_property = {'some_key': 'one_item'}

    def test_max_setting(self):
        schema = {
            'str_max_property': {'type': 'str', 'max': 5},
            'int_max_property': {'type': 'int', 'max': 10},
            'float_max_property': {'type': 'float', 'max': 20},
            'list_max_property': {'type': 'list', 'max': 1},
            'set_max_property': {'type': 'set', 'max': 1},
            'dict_max_property': {'type': 'dict', 'max': 1},
        }

        ook_type = object_tools.create_ook_type('Maxer', schema)
        self.assertIsNotNone(ook_type)
        object_tools.validate_schema(ook_type.get_schema())

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
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)
        ook_object.str_max_property = 'small'

        # Int failure
        ook_object.int_max_property = 20
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)
        ook_object.int_max_property = 5

        # Float failure
        ook_object.float_max_property = 30.0
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)
        ook_object.float_max_property = 15.0

        # List failure
        ook_object.list_max_property = ['one item', 'two item']
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)
        ook_object.list_max_property = ['one item']

        # Set failure
        ook_object.set_max_property = {'one item', 'two item'}
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)
        ook_object.set_max_property = {'one item'}

        # Dict failure
        ook_object.dict_max_property = {'some_key': 'one_item', 'another_key': 'two_item'}
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)
        ook_object.dict_max_property = {'some_key': 'one_item'}
