"""OnticProperty unit tests."""
from copy import copy, deepcopy

from ontic.ontic_property import (OnticProperty, 
                                  perfect_property, 
                                  validate_property)
from ontic.validation_exception import ValidationException

from test.utils import BaseTestCase


class OnticPropertyTest(BaseTestCase):
    """OnticProperty test cases."""

    def test_ontic_property_instantiation(self):
        """OnticProperty instantiation testing to confirm dict behaviour."""
        ontic_property1 = OnticProperty()
        self.assertIsNotNone(ontic_property1)

        # Test dictionary initialization.
        ontic_property2 = OnticProperty(
            {
                'type': int,
                'default': 1,
                'required': True
            }
        )
        self.assertIsNotNone(ontic_property2)
        self.assertEqual(int, ontic_property2['type'])
        self.assertEqual(1, ontic_property2.default)
        self.assertEqual(True, ontic_property2['required'])

        # Test initialization by property.
        ontic_property3 = OnticProperty(
            type=int,
            default=1,
            required=True)
        self.assertIsNotNone(ontic_property3)
        self.assertEqual(int, ontic_property3.type)
        self.assertEqual(1, ontic_property3['default'])
        self.assertEqual(True, ontic_property3.required)

        # Test initialization by list.
        ontic_property4 = OnticProperty(
            [['type', int], ['default', 1], ['required', True]])
        self.assertIsNotNone(ontic_property4)
        self.assertEqual(int, ontic_property4['type'])
        self.assertEqual(1, ontic_property4.default)
        self.assertEqual(True, ontic_property4['required'])

    def test_dynamic_access(self):
        """Ensure OnticProperty property access as dict and attribute."""
        the_property = OnticProperty()
        self.assert_dynamic_accessing(the_property)

    def test_copy(self):
        """Ensure that OnticProperty supports copy operations."""

        # Create the test data.
        ontic_property = OnticProperty(
            type=str,
            required=False,
            enum={'dog', 'cat'},
        )

        # Execute the test.
        property_copy = copy(ontic_property)

        # Validate the test results.
        self.assertIsNot(ontic_property, property_copy)
        self.assertIs(ontic_property.type, property_copy.type)
        self.assertIs(ontic_property.required, property_copy.required)
        self.assertSetEqual(ontic_property.enum, property_copy.enum)

    def test_deepcopy(self):
        """Ensure that OnticMeta supports deepcopy operation."""

        # Create the test data.
        ontic_property = OnticProperty(
            type=str,
            required=False,
            enum={'dog', 'cat'},
        )

        # Execute the test.
        property_copy = deepcopy(ontic_property)

        # Validate the test results.
        self.assertIsNot(ontic_property, property_copy)
        self.assertIs(ontic_property.type, property_copy.type)
        self.assertIs(ontic_property.required, property_copy.required)
        self.assertSetEqual(ontic_property.enum, property_copy.enum)

    def test_property_type_instantiation_failure(self):
        """Validate error reporting for bad OnticProperty definition."""

        bad_schema_test_case = {'type': 'UNDEFINED'}

        self.assertRaisesRegexp(
            ValueError,
            r"""Illegal type declaration: UNDEFINED""",
            OnticProperty, bad_schema_test_case)

        class UNDEFINED(object):
            pass

        bad_schema_test_case = {'type': UNDEFINED}

        self.assertRaisesRegexp(
            ValueError,
            r"""Illegal type declaration: %s""" % UNDEFINED,
            OnticProperty, bad_schema_test_case)

    def test_property_type_validate(self):
        """Test OnticProperty.validate method."""
        property_schema = OnticProperty()
        self.assertIsNotNone(property_schema)

        property_schema.type = int
        self.assertEqual([], property_schema.validate())

        property_schema.type = '__WRONG__'
        self.assertRaises(ValidationException, property_schema.validate)

    def test_property_schema_perfect(self):
        """Test OnticProperty.perfect method."""
        candidate_schema_property = OnticProperty()
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

        # Remove a property and ensure perfect returns it.
        delattr(candidate_schema_property, 'type')
        self.assertEqual(9, len(candidate_schema_property))

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
        candidate_schema_property = OnticProperty(
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

        # Remove a property and ensure perfect returns it.
        delattr(candidate_schema_property, 'enum')
        self.assertEqual(9, len(candidate_schema_property))

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


class PerfectSchemaPropertyTestCase(BaseTestCase):
    """Test cases for the perfect_property method."""

    def test_perfect_empty_schema_property(self):
        """Validate the perfection of an empty schema property."""
        candidate_schema_property = OnticProperty()
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

        # Remove a property and ensure perfect returns it.
        delattr(candidate_schema_property, 'type')
        self.assertEqual(9, len(candidate_schema_property))

        perfect_property(candidate_schema_property)

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
        candidate_schema_property = OnticProperty(
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

        # Remove a property and ensure perfect returns it.
        delattr(candidate_schema_property, 'min')
        self.assertEqual(9, len(candidate_schema_property))

        perfect_property(candidate_schema_property)

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
        perfect_property."""
        self.assertRaisesRegexp(
            ValueError,
            '"ontic_property" must be provided.',
            perfect_property, None)

        self.assertRaisesRegexp(
            ValueError,
            '"ontic_property" must be OnticProperty type.',
            perfect_property, {})


class ValidateSchemaProperty(BaseTestCase):
    """Various tests of the 'validate_property_type' method."""

    def test_bad_validate_schema_property_call(self):
        """Test bad use cases of validate_property_type function call."""
        self.assertRaisesRegexp(
            ValueError,
            '"ontic_property" must be provided.',
            validate_property, None, list())

        self.assertRaisesRegexp(
            ValueError,
            '"ontic_property" must be OnticProperty type.',
            validate_property, dict(), list())

    def test_validate_schema_property_exception(self):
        """Test validate_schema validation exception handling."""
        invalid_property_schema = OnticProperty()
        invalid_property_schema.type = 'UNKNOWN'

        self.maxDiff = None
        self.assertRaisesRegexp(
            ValidationException,
            r"""The value "UNKNOWN" for "type" not in enumeration \[.*\].""",
            validate_property, invalid_property_schema)

        value_errors = validate_property(
            invalid_property_schema,
            raise_validation_exception=False)
        self.assertEqual(1, len(value_errors))
        self.assertTrue(value_errors[0].startswith(
            'The value "UNKNOWN" for "type" not in enumeration'))
