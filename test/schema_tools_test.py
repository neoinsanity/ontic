from test_utils import base_test_case

from ook import schema_tools
from ook.schema_type import SchemaProperty, SchemaType


class ValidateSchemaProperty(base_test_case.BaseTestCase):
    def test_bad_validate_schema_property(self):
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema_property" must be provided.',
            schema_tools.validate_schema_property, None)

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema_property" must be SchemaProperty type.',
            schema_tools.validate_schema_property, {})


class ValidateSchemaTestCase(base_test_case.BaseTestCase):
    """Test schema_tools.validate_schema method."""

    def test_bad_validate_schema(self):
        """ValueError testing of validate_schema."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be provided.',
            schema_tools.validate_schema, None)
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be of SchemaType.',
            schema_tools.validate_schema, "not a schema")

    def test_validate_schema(self):
        """Valid schema testing of validate_schema."""
        schema = SchemaType({'some_property': {'type': 'int'}})

        # Dict test
        schema_tools.validate_schema(schema)

        # BaseType test
        base_type_schema = SchemaType(schema)
        schema_tools.validate_schema(base_type_schema)

        # SchemaType test
        schema_type_schema = SchemaType(schema)
        schema_tools.validate_schema(schema_type_schema)


class PerfectSchemaPropertyTestCase(base_test_case.BaseTestCase):
    def test_perfect_empty_schema_property(self):
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

        schema_tools.perfect_schema_property(candidate_schema_property)

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

        schema_tools.perfect_schema_property(candidate_schema_property)

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
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema_property" must be provided.',
            schema_tools.perfect_schema_property, None)

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema_property" must be SchemaProperty type.',
            schema_tools.perfect_schema_property, {})


class PerfectSchemaTestCase(base_test_case.BaseTestCase):
    def test_perfect_schema_type(self):
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

        schema_tools.perfect_schema(candidate_schema)

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
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be provided.',
            schema_tools.perfect_schema, None)

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be of SchemaType.',
            schema_tools.perfect_schema, {})
