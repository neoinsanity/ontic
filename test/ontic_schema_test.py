"""Test the basic functionality of the schema data types."""

from copy import copy, deepcopy

from test.utils import BaseTestCase

from ontic.ontic_property import OnticProperty
from ontic import ontic_schema
from ontic.ontic_schema import Schema
from ontic.validation_exception import ValidationException


class OnticSchemaTest(BaseTestCase):
    """Schema test cases."""

    def test_ontic_schema_instantiation(self):
        """Core instantiation to confirm dict behavior."""
        schema1 = Schema()
        self.assertIsNotNone(schema1)
        self.assertDictEqual({}, schema1)

        # Test dictionary initialization.
        schema2 = Schema({'prop1': {}, 'prop2': {'type': 'int'}})
        self.assertIsNotNone(schema2)
        self.assertIsInstance(schema2['prop1'], OnticProperty)
        self.assertEqual(
            {
                'max': None, 'regex': None, 'default': None, 'member_min': None,
                'member_max': None, 'required': False, 'member_type': None,
                'enum': None, 'type': None, 'min': None, 'name': 'prop1'
            },
            schema2['prop1'])
        self.assertIsInstance(schema2.prop2, OnticProperty)
        self.assertEqual(
            {
                'default': None, 'min': None, 'max': None, 'enum': None,
                'type': int, 'member_max': None, 'member_type': None,
                'required': False, 'regex': None, 'member_min': None,
                'name': 'prop2'
            },
            schema2.prop2)

        # Test initialization by property.
        schema3 = Schema(prop1={}, prop2={'type': 'str'})
        self.assertIsNotNone(schema3)
        self.assertIsInstance(schema3.prop1, OnticProperty)
        self.assertDictEqual(
            {
                'min': None, 'type': None, 'regex': None, 'member_max': None,
                'member_min': None, 'member_type': None, 'enum': None,
                'max': None, 'name': 'prop1',
                'required': False, 'default': None
            },
            schema3.prop1)
        self.assertIsInstance(schema3.prop2, OnticProperty)
        self.assertDictEqual(
            {
                'min': None, 'type': str, 'regex': None, 'member_max': None,
                'member_min': None, 'member_type': None, 'enum': None,
                'max': None, 'name': 'prop2',
                'required': False, 'default': None
            },
            schema3['prop2'])

        # Test initialization by list.
        schema4 = Schema([['prop1', {}], ['prop2', {'type': bool}]])
        self.assertIsNotNone(schema4)
        self.assertIsInstance(schema4.prop1, OnticProperty)
        self.assertEqual(
            {
                'member_max': None, 'member_min': None, 'enum': None,
                'regex': None, 'required': False, 'min': None,
                'max': None, 'default': None, 'type': None,
                'member_type': None, 'name': 'prop1'
            },
            schema4['prop1'])
        self.assertIsInstance(schema4.prop2, OnticProperty)
        self.assertEqual(
            {
                'member_max': None, 'member_min': None, 'enum': None,
                'regex': None, 'required': False, 'min': None,
                'max': None, 'default': None, 'type': bool,
                'member_type': None, 'name': 'prop2'
            },
            schema4.prop2)

    def test_dynamic_access(self):
        """Core property access as a dict and as attribute."""
        schema = Schema()
        self.assert_dynamic_accessing(schema)

    def test_copy(self):
        """Ensure that Core supports copy operations."""

        # Create the test data.
        some_schema = Schema([
            {'name': 'int_prop', 'type': 'int'},
            {'name': 'str_prop', 'type': str},
            OnticProperty({'name': 'list_prop', 'type': list}),
        ])

        # Execute the test.
        schema_copy = copy(some_schema)

        # Validate the test results.
        self.assertIsInstance(schema_copy, Schema)
        self.assertIsNot(schema_copy, some_schema)
        self.assertDictEqual(schema_copy, some_schema)
        self.assertIs(schema_copy.int_prop, some_schema.int_prop)
        self.assertIs(schema_copy.str_prop, some_schema.str_prop)
        self.assertIs(schema_copy.list_prop, some_schema.list_prop)

    def test_deepcopy(self):
        """Ensure that Core supports deepcopy operation."""

        # Create the test data.
        some_schema = Schema([
            {'name': 'int_prop', 'type': 'int'},
            {'name': 'str_prop', 'type': str},
            OnticProperty({'name': 'list_prop', 'type': list}),
        ])

        # Execute the test.
        schema_copy = deepcopy(some_schema)

        # Validate the test results.
        self.assertIsInstance(schema_copy, Schema)
        self.assertIsNot(schema_copy, some_schema)
        self.assertDictEqual(schema_copy, some_schema)
        self.assertIsNot(schema_copy.int_prop, some_schema.int_prop)
        self.assertIsNot(schema_copy.str_prop, some_schema.str_prop)
        self.assertIsNot(schema_copy.list_prop, some_schema.list_prop)

    def test_schema_definition(self):
        """Schema instantiation testing to confirm dict behaviour."""
        schema_object = Schema()
        self.assertIsNotNone(schema_object)

        schema_object = Schema({
            'property1': {}
        })
        self.assertIsNotNone(schema_object)
        self.assertTrue(hasattr(schema_object, 'property1'))
        self.assertTrue('property1' in schema_object)

    def test_ontic_schema_perfect(self):
        """Test the Schema.perfect method."""
        some_schema = Schema([
            OnticProperty(name='prop1'),
            OnticProperty({'name': 'prop2', 'type': 'str', 'min': 5})
        ])
        self.assertEqual(2, len(some_schema))
        self.assertEqual(11, len(some_schema.prop1))
        self.assertEqual(11, len(some_schema.prop2))
        self.maxDiff = None
        self.assertDictEqual(
            {
                'prop1': {
                    'name': 'prop1',
                    'regex': None,
                    'member_max': None,
                    'enum': None,
                    'min': None,
                    'default': None,
                    'max': None,
                    'required': False,
                    'member_min': None,
                    'member_type': None,
                    'type': None
                },
                'prop2': {
                    'name': 'prop2',
                    'regex': None,
                    'member_max': None,
                    'enum': None,
                    'min': 5.0,
                    'default': None,
                    'max': None,
                    'required': False,
                    'member_min': None,
                    'member_type': None,
                    'type': str
                }},
            some_schema)

        some_schema.perfect()

        self.assertEqual(2, len(some_schema))
        self.assertEqual(11, len(some_schema.prop1))
        self.assertEqual(11, len(some_schema.prop2))
        self.assertDictEqual(
            {
                'prop1': {
                    'name': 'prop1',
                    'default': None,
                    'enum': None,
                    'member_max': None,
                    'member_min': None,
                    'member_type': None,
                    'max': None,
                    'min': None,
                    'regex': None,
                    'required': False,
                    'type': None
                },
                'prop2': {
                    'name': 'prop2',
                    'default': None,
                    'enum': None,
                    'member_max': None,
                    'member_min': None,
                    'member_type': None,
                    'max': None,
                    'min': 5.0,
                    'regex': None,
                    'required': False,
                    'type': str
                }
            }, some_schema)
        self.assertIsInstance(some_schema.prop1, OnticProperty)
        self.assertIsInstance(some_schema.prop2, OnticProperty)

    def test_ontic_schema_validate(self):
        """Test the Schema.validate method."""
        schema = Schema({'some_property': {'type': 'int'}})

        # Dict test
        self.assertEqual([], schema.validate())

        # OnticType test
        base_type_schema = Schema(schema)
        ontic_schema.validate_schema(base_type_schema)

        # Schema test
        ontic_schema_schema = Schema(schema)
        ontic_schema.validate_schema(ontic_schema_schema)


class ValidateSchemaTestCase(BaseTestCase):
    """Test ontic_schemas.validate_schema method."""

    def test_bad_validate_schema(self):
        """ValueError testing of validate_schema."""
        self.assertRaisesRegexp(
            ValueError,
            r""""ontic_schema" argument must be provided.""",
            ontic_schema.validate_schema, None)
        self.assertRaisesRegexp(
            ValueError,
            r""""ontic_schema" argument must be of Schema type.""",
            ontic_schema.validate_schema, "not a schema")

    def test_validate_schema(self):
        """Valid schema testing of validate_schema."""
        schema = Schema({'some_property': {'type': 'int'}})

        # Dict test
        ontic_schema.validate_schema(schema)

        # OnticType test
        base_type_schema = Schema(schema)
        ontic_schema.validate_schema(base_type_schema)

        # Schema test
        ontic_schema_schema = Schema(schema)
        ontic_schema.validate_schema(ontic_schema_schema)

    def test_validate_schema_exception_handling(self):
        """Ensure validate_schema covers basic exception reporting."""
        property_schema = OnticProperty(name='some_attr')
        property_schema.required = 'UNDEFINED'
        schema_instance = Schema()
        schema_instance.add(property_schema)

        self.assertRaisesRegexp(
            ValidationException,
            r"""The value for "required" is not """
            r"""of type "<class 'bool'>": UNDEFINED""",
            ontic_schema.validate_schema, schema_instance)

        expected_errors_list = [
            """The value for "required" is not of """
            """type "<class 'bool'>": UNDEFINED"""]
        try:
            ontic_schema.validate_schema(schema_instance)
            self.fail('A ValidationException should have been thrown.')
        except ValidationException as ve:
            self.assertListEqual(expected_errors_list, ve.validation_errors)

        errors = ontic_schema.validate_schema(
            schema_instance,
            raise_validation_exception=False)
        self.assertListEqual(expected_errors_list, errors)


class PerfectSchemaTestCase(BaseTestCase):
    """Test cases for use of the perfect_schema method."""

    def test_perfect_ontic_schema(self):
        """Validate 'perfect_schema' method usage."""
        schema_def = [
            OnticProperty(name='prop1'),
            OnticProperty({'name': 'prop2', 'type': 'str', 'min': 5})
        ]
        some_schema = Schema(schema_def)
        self.assertEqual(2, len(some_schema))
        self.assertEqual(11, len(some_schema.prop1))
        self.assertEqual(11, len(some_schema.prop2))
        self.maxDiff = None
        self.assertDictEqual(
            {
                'prop1': {
                    'name': 'prop1',
                    'regex': None,
                    'member_max': None,
                    'enum': None,
                    'min': None,
                    'default': None,
                    'max': None,
                    'required': False,
                    'member_min': None,
                    'member_type': None,
                    'type': None
                },
                'prop2': {
                    'name': 'prop2',
                    'regex': None,
                    'member_max': None,
                    'enum': None,
                    'min': 5.0,
                    'default': None,
                    'max': None,
                    'required': False,
                    'member_min': None,
                    'member_type': None,
                    'type': str
                }},
            some_schema)

        ontic_schema.perfect_schema(some_schema)

        self.assertEqual(2, len(some_schema))
        self.assertEqual(11, len(some_schema.prop1))
        self.assertEqual(11, len(some_schema.prop2))
        self.assertDictEqual(
            {
                'prop1': {
                    'name': 'prop1',
                    'default': None,
                    'enum': None,
                    'member_max': None,
                    'member_min': None,
                    'member_type': None,
                    'max': None,
                    'min': None,
                    'regex': None,
                    'required': False,
                    'type': None
                },
                'prop2': {
                    'name': 'prop2',
                    'default': None,
                    'enum': None,
                    'member_max': None,
                    'member_min': None,
                    'member_type': None,
                    'max': None,
                    'min': 5.0,
                    'regex': None,
                    'required': False,
                    'type': str
                }
            }, some_schema)
        self.assertIsInstance(some_schema.prop1, OnticProperty)
        self.assertIsInstance(some_schema.prop2, OnticProperty)

    def test_bad_perfect_schema(self):
        """Validate proper error handling in 'perfect_schema' method."""
        self.assertRaisesRegexp(
            ValueError,
            r""""ontic_schema" must be provided.""",
            ontic_schema.perfect_schema, None)

        self.assertRaisesRegexp(
            ValueError,
            r""""ontic_schema" argument must be of Schema type.""",
            ontic_schema.perfect_schema, {})
