from test_utils import base_test_case

from ook.meta_type import SchemaProperty
from ook import schema_type
from ook.schema_type import SchemaType


class ValidateSchemaProperty(base_test_case.BaseTestCase):
    """Various tests of the 'validate_schema_property' method."""

    def test_bad_validate_schema_property(self):
        """Test bad use cases of validate_schema_property."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema_property" must be provided.',
            SchemaProperty.validate_schema_property, None)

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema_property" must be SchemaProperty type.',
            SchemaProperty.validate_schema_property, {})


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

        # BaseType test
        base_type_schema = SchemaType(schema)
        schema_type.validate_schema(base_type_schema)

        # SchemaType test
        schema_type_schema = SchemaType(schema)
        schema_type.validate_schema(schema_type_schema)


class PerfectSchemaPropertyTestCase(base_test_case.BaseTestCase):
    """Test cases for the perfect_schema_property method."""

    def test_perfect_empty_schema_property(self):
        """Validate the perfection of an empty schema property."""
        candidate_schema_property = SchemaProperty()
        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
                'default': False,
                'enum': None,
                'item_max': None,
                'item_min': None,
                'item_type': None,
                'max': None,
                'min': None,
                'regex': None,
                'required': False,
                'type': None
            },
            candidate_schema_property)

        SchemaProperty.perfect_schema_property(candidate_schema_property)

        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
                'regex': None,
                'item_max': None,
                'enum': None,
                'min': None,
                'default': False,
                'max': None,
                'required': False,
                'item_min': None,
                'item_type': None,
                'type': None
            }, candidate_schema_property)

    def test_perfect_partial_schema_property(self):
        """Validate the perfection of a partial schema definition."""
        candidate_schema_property = SchemaProperty(
            {
                'type': 'int',
                'required': True,
                'UNRECOGNIZED': 'irrelevant',
            })
        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
                'regex': None,
                'item_max': None,
                'enum': None,
                'min': None,
                'default': False,
                'max': None,
                'required': True,
                'item_min': None,
                'item_type': None,
                'type': 'int'
            },
            candidate_schema_property)

        SchemaProperty.perfect_schema_property(candidate_schema_property)

        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
                'regex': None,
                'item_max': None,
                'enum': None,
                'min': None,
                'default': False,
                'max': None,
                'required': True,
                'item_min': None,
                'item_type': None,
                'type': 'int'
            }, candidate_schema_property)

    def test_bad_perfect_schema_property(self):
        """Validate error handling for bad schemas passed to perfect_schema_property."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema_property" must be provided.',
            SchemaProperty.perfect_schema_property, None)

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema_property" must be SchemaProperty type.',
            SchemaProperty.perfect_schema_property, {})


class PerfectSchemaTestCase(base_test_case.BaseTestCase):
    """Test cases for use of the perfect_schema method."""

    def test_perfect_schema_type(self):
        """Validate 'perfect_schema' method usage."""
        candidate_schema = SchemaType({
            'prop1': SchemaProperty(),
            'prop2': SchemaProperty({'type': 'str', 'min': 5})
        })
        self.assertEqual(2, len(candidate_schema))
        self.assertEqual(10, len(candidate_schema.prop1))
        self.assertEqual(10, len(candidate_schema.prop2))
        self.maxDiff = None
        self.assertDictEqual(
            {
                'prop1': {
                    'regex': None,
                    'item_max': None,
                    'enum': None,
                    'min': None,
                    'default': False,
                    'max': None,
                    'required': False,
                    'item_min': None,
                    'item_type': None,
                    'type': None
                },
                'prop2': {
                    'regex': None,
                    'item_max': None,
                    'enum': None,
                    'min': 5,
                    'default': False,
                    'max': None,
                    'required': False,
                    'item_min': None,
                    'item_type': None,
                    'type': 'str'
                }},
            candidate_schema)

        schema_type.perfect_schema(candidate_schema)

        self.assertEqual(2, len(candidate_schema))
        self.assertEqual(10, len(candidate_schema.prop1))
        self.assertEqual(10, len(candidate_schema.prop2))
        self.assertDictEqual(
            {
                'prop1': {'default': False,
                          'enum': None,
                          'item_max': None,
                          'item_min': None,
                          'item_type': None,
                          'max': None,
                          'min': None,
                          'regex': None,
                          'required': False,
                          'type': None
                },
                'prop2': {'default': False,
                          'enum': None,
                          'item_max': None,
                          'item_min': None,
                          'item_type': None,
                          'max': None,
                          'min': 5,
                          'regex': None,
                          'required': False,
                          'type': 'str'
                }
            }, candidate_schema)
        self.assertIsInstance(candidate_schema.prop1, SchemaProperty)
        self.assertIsInstance(candidate_schema.prop2, SchemaProperty)

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
