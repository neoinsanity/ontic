import base_test_case

from ook import schema_tools
from ook.schema_type import SchemaProperty, SchemaType


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
