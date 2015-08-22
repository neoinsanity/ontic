"""Test the basic functionality of the schema data types."""

from test_utils import base_test_case

from ontic.property_type import PropertyType
from ontic import schema_type
from ontic.schema_type import SchemaType
from ontic.validation_exception import ValidationException


class SchemaTypeTest(base_test_case.BaseTestCase):
    """SchemaType test cases."""

    def test_schema_definition(self):
        """SchemaType instantiation testing to confirm dict behaviour."""
        schema_object = SchemaType()
        self.assertIsNotNone(schema_object)

        schema_object = SchemaType({
            'property1': {}
        })
        self.assertIsNotNone(schema_object)
        self.assertTrue(hasattr(schema_object, 'property1'))
        self.assertTrue('property1' in schema_object)

    def test_schema_type_perfect(self):
        """Test the SchemaType.perfect method."""
        candidate_schema = SchemaType({
            'prop1': PropertyType(),
            'prop2': PropertyType({'type': 'str', 'min': 5})
        })
        self.assertEqual(2, len(candidate_schema))
        self.assertEqual(10, len(candidate_schema.prop1))
        self.assertEqual(10, len(candidate_schema.prop2))
        self.maxDiff = None
        self.assertDictEqual(
            {
                'prop1': {
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
            candidate_schema)

        candidate_schema.perfect()

        self.assertEqual(2, len(candidate_schema))
        self.assertEqual(10, len(candidate_schema.prop1))
        self.assertEqual(10, len(candidate_schema.prop2))
        self.assertDictEqual(
            {
                'prop1': {
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
            }, candidate_schema)
        self.assertIsInstance(candidate_schema.prop1, PropertyType)
        self.assertIsInstance(candidate_schema.prop2, PropertyType)

    def test_schema_type_validate(self):
        """Test the SchemaType.validate method."""
        schema = SchemaType({'some_property': {'type': 'int'}})

        # Dict test
        self.assertEqual([], schema.validate())

        # OnticType test
        base_type_schema = SchemaType(schema)
        schema_type.validate_schema(base_type_schema)

        # SchemaType test
        schema_type_schema = SchemaType(schema)
        schema_type.validate_schema(schema_type_schema)


class ValidateSchemaTestCase(base_test_case.BaseTestCase):
    """Test schema_types.validate_schema method."""

    def test_bad_validate_schema(self):
        """ValueError testing of validate_schema."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be provided.',
            schema_type.validate_schema, None)
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be of SchemaType.',
            schema_type.validate_schema, "not a schema")

    def test_validate_schema(self):
        """Valid schema testing of validate_schema."""
        schema = SchemaType({'some_property': {'type': 'int'}})

        # Dict test
        schema_type.validate_schema(schema)

        # OnticType test
        base_type_schema = SchemaType(schema)
        schema_type.validate_schema(base_type_schema)

        # SchemaType test
        schema_type_schema = SchemaType(schema)
        schema_type.validate_schema(schema_type_schema)

    def test_validate_schema_exception_handling(self):
        """Ensure validate_schema covers basic exception reporting."""
        property_schema = PropertyType()
        property_schema.required = 'UNDEFINED'
        schema_instance = SchemaType()
        schema_instance.some_attr = property_schema

        self.assertRaisesRegexp(
            ValidationException,
            r"""The value for "required" is not """
            r"""of type "<type 'bool'>": UNDEFINED""",
            schema_type.validate_schema, schema_instance)

        expected_errors_list = [
            """The value for "required" is not of """
            """type "<type 'bool'>": UNDEFINED"""]

        try:
            schema_type.validate_schema(schema_instance)
            self.fail('A ValidationException should have been thrown.')
        except ValidationException as ve:
            self.assertListEqual(expected_errors_list, ve.validation_errors)

        errors = schema_type.validate_schema(
            schema_instance,
            raise_validation_exception=False)
        self.assertListEqual(expected_errors_list, errors)


class PerfectSchemaTestCase(base_test_case.BaseTestCase):
    """Test cases for use of the perfect_schema method."""

    def test_perfect_schema_type(self):
        """Validate 'perfect_schema' method usage."""
        candidate_schema = SchemaType({
            'prop1': PropertyType(),
            'prop2': PropertyType({'type': 'str', 'min': 5})
        })
        self.assertEqual(2, len(candidate_schema))
        self.assertEqual(10, len(candidate_schema.prop1))
        self.assertEqual(10, len(candidate_schema.prop2))
        self.maxDiff = None
        self.assertDictEqual(
            {
                'prop1': {
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
            candidate_schema)

        schema_type.perfect_schema(candidate_schema)

        self.assertEqual(2, len(candidate_schema))
        self.assertEqual(10, len(candidate_schema.prop1))
        self.assertEqual(10, len(candidate_schema.prop2))
        self.assertDictEqual(
            {
                'prop1': {
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
            }, candidate_schema)
        self.assertIsInstance(candidate_schema.prop1, PropertyType)
        self.assertIsInstance(candidate_schema.prop2, PropertyType)

    def test_bad_perfect_schema(self):
        """Validate proper error handling in 'perfect_schema' method."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be provided.',
            schema_type.perfect_schema, None)

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be of SchemaType.',
            schema_type.perfect_schema, {})
