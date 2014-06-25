from test_utils import base_test_case

from ook.meta_type import PropertySchema
from ook.schema_type import SchemaType


class ValidateSchemaProperty(base_test_case.BaseTestCase):
    """Various tests of the 'validate_schema_property' method."""

    def test_bad_validate_schema_property(self):
        """Test bad use cases of validate_schema_property."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema_property" must be provided.',
            PropertySchema.validate_schema_property, None, list())

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema_property" must be PropertySchema type.',
            PropertySchema.validate_schema_property, dict(), list())


class ValidateSchemaTestCase(base_test_case.BaseTestCase):
    """Test schema_types.validate_schema method."""

    def test_bad_validate_schema(self):
        """ValueError testing of validate_schema."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be provided.',
            SchemaType.validate_schema, None)
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be of SchemaType.',
            SchemaType.validate_schema, "not a schema")

    def test_validate_schema(self):
        """Valid schema testing of validate_schema."""
        schema = SchemaType({'some_property': {'type': 'int'}})

        # Dict test
        SchemaType.validate_schema(schema)

        # ObjectType test
        base_type_schema = SchemaType(schema)
        SchemaType.validate_schema(base_type_schema)

        # SchemaType test
        schema_type_schema = SchemaType(schema)
        SchemaType.validate_schema(schema_type_schema)


class PerfectSchemaPropertyTestCase(base_test_case.BaseTestCase):
    """Test cases for the perfect_schema_property method."""

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

        PropertySchema.perfect_schema_property(candidate_schema_property)

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
                'type': 'int'
            },
            candidate_schema_property)

        PropertySchema.perfect_schema_property(candidate_schema_property)

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
                'type': 'int'
            }, candidate_schema_property)

    def test_bad_perfect_schema_property(self):
        """Validate error handling for bad schemas passed to
        perfect_schema_property."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema_property" must be provided.',
            PropertySchema.perfect_schema_property, None)

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema_property" must be PropertySchema type.',
            PropertySchema.perfect_schema_property, {})


class PerfectSchemaTestCase(base_test_case.BaseTestCase):
    """Test cases for use of the perfect_schema method."""

    def test_perfect_schema_type(self):
        """Validate 'perfect_schema' method usage."""
        candidate_schema = SchemaType({
            'prop1': PropertySchema(),
            'prop2': PropertySchema({'type': 'str', 'min': 5})
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
                    'min': 5,
                    'default': None,
                    'max': None,
                    'required': False,
                    'member_min': None,
                    'member_type': None,
                    'type': 'str'
                }},
            candidate_schema)

        SchemaType.perfect_schema(candidate_schema)

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
                    'min': 5,
                    'regex': None,
                    'required': False,
                    'type': 'str'
                }
            }, candidate_schema)
        self.assertIsInstance(candidate_schema.prop1, PropertySchema)
        self.assertIsInstance(candidate_schema.prop2, PropertySchema)

    def test_bad_perfect_schema(self):
        """Validate proper error handling in 'perfect_schema' method."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be provided.',
            SchemaType.perfect_schema, None)

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be of SchemaType.',
            SchemaType.perfect_schema, {})
