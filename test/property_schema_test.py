from test.test_utils import base_test_case

from ontic.property_schema import PropertySchema, validate_property_schema
from ontic.validation_exception import ValidationException


class PropertySchemaTest(base_test_case.BaseTestCase):
    """PropertySchema test cases"""

    def test_property_schema_instantiation(self):
        """PropertySchema instantiation testing to confirm dict behavior."""
        property_schema = PropertySchema()
        self.assertIsNotNone(property_schema)

        expected_schema = {
            'default': None,
            'enum': None,
            'max': 7,
            'member_max': None,
            'member_min': None,
            'member_type': None,
            'min': 3,
            'regex': None,
            'required': True,
            'type': int,
        }

        property_schema = PropertySchema({
            'type': 'int',
            'required': True,
            'min': 3,
            'max': 7,
        })
        self.assertIsNotNone(property_schema)
        self.assertDictEqual(expected_schema, property_schema)

        property_schema = PropertySchema(
            type='int', required=True, min=3, max=7)
        self.assertIsNotNone(property_schema)
        self.assertDictEqual(expected_schema, property_schema)

        property_schema = PropertySchema(
            [['type', 'int'], ['required', True], ['min', 3], ['max', 7]])
        self.assertIsNotNone(property_schema)
        self.assertDictEqual(expected_schema, property_schema)

    def test_property_schema_instantiation_failure(self):
        """Validate error reporting for bad PropertySchema definition."""

        bad_schema_test_case = {'type': 'UNDEFINED'}

        self.assertRaisesRegexp(
            ValueError,
            r"""Illegal type declaration: UNDEFINED""",
            PropertySchema, bad_schema_test_case)


class ValidateSchemaProperty(base_test_case.BaseTestCase):
    """Various tests of the 'validate_property_schema' method."""

    def test_bad_validate_schema_property_call(self):
        """Test bad use cases of validate_property_schema function call."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_property_schema" must be provided.',
            validate_property_schema, None, list())

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_property_schema" must be PropertySchema type.',
            validate_property_schema, dict(), list())

    def test_validate_schema_property_exception(self):
        """Test validate_schema validation exception handling."""
        invalid_property_schema = PropertySchema()
        invalid_property_schema.type = 'UNKNOWN'

        self.maxDiff = None
        self.assertRaisesRegexp(
            ValidationException,
            r"""The value "UNKNOWN" for "type" not in enumeration \[.*\].""",
            validate_property_schema, invalid_property_schema)

        value_errors = validate_property_schema(
            invalid_property_schema,
            raise_validation_exception=False)
        self.assertEqual(1, len(value_errors))
        self.assertTrue(value_errors[0].startswith(
            'The value "UNKNOWN" for "type" not in enumeration'))
