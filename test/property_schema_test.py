from test.test_utils import base_test_case

from ontic.property_schema import (PropertySchema, perfect_property_schema,
                                   validate_property_schema)
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

    def test_property_schema_validate(self):
        """Test PropertySchema.validate method."""
        property_schema = PropertySchema()
        self.assertIsNotNone(property_schema)

        property_schema.type = int
        self.assertEqual([], property_schema.validate())

        property_schema.type = '__WRONG__'
        self.assertRaises(ValidationException, property_schema.validate)


    def test_property_schema_perfect(self):
        """Test PropertySchema.perfect method."""
        candidate_schema_property = PropertySchema()
        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
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
            candidate_schema_property)

        candidate_schema_property.perfect()

        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
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
            }, candidate_schema_property)

    def test_perfect_partial_schema_property(self):
        """Validate the perfection of a partial schema definition."""
        candidate_schema_property = PropertySchema(
            {
                'type': 'int',
                'required': True,
                'UNRECOGNIZED': 'irrelevant',
            })
        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
                'regex': None,
                'member_max': None,
                'enum': None,
                'min': None,
                'default': None,
                'max': None,
                'required': True,
                'member_min': None,
                'member_type': None,
                'type': int
            },
            candidate_schema_property)

        candidate_schema_property.perfect()

        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
                'regex': None,
                'member_max': None,
                'enum': None,
                'min': None,
                'default': None,
                'max': None,
                'required': True,
                'member_min': None,
                'member_type': None,
                'type': int
            }, candidate_schema_property)


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


class PerfectSchemaPropertyTestCase(base_test_case.BaseTestCase):
    """Test cases for the perfect_property_schema method."""

    def test_perfect_empty_schema_property(self):
        """Validate the perfection of an empty schema property."""
        candidate_schema_property = PropertySchema()
        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
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
            candidate_schema_property)

        perfect_property_schema(candidate_schema_property)

        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
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
            }, candidate_schema_property)

    def test_perfect_partial_schema_property(self):
        """Validate the perfection of a partial schema definition."""
        candidate_schema_property = PropertySchema(
            {
                'type': 'int',
                'required': True,
                'UNRECOGNIZED': 'irrelevant',
            })
        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
                'regex': None,
                'member_max': None,
                'enum': None,
                'min': None,
                'default': None,
                'max': None,
                'required': True,
                'member_min': None,
                'member_type': None,
                'type': int
            },
            candidate_schema_property)

        perfect_property_schema(candidate_schema_property)

        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
                'regex': None,
                'member_max': None,
                'enum': None,
                'min': None,
                'default': None,
                'max': None,
                'required': True,
                'member_min': None,
                'member_type': None,
                'type': int
            }, candidate_schema_property)

    def test_bad_perfect_schema_property(self):
        """Validate error handling for bad schemas passed to
        perfect_property_schema."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_property_schema" must be provided.',
            perfect_property_schema, None)

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_property_schema" must be PropertySchema type.',
            perfect_property_schema, {})
