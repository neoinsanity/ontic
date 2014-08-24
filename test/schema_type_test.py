"""Test the basic functionality of the schema data types."""

from test_utils import base_test_case

from ontic.meta_type import PropertySchema
from ontic.schema_type import SchemaType


class SchemaPropertyTest(base_test_case.BaseTestCase):
    """PropertySchema test cases."""

    def test_schema_property_instantiation(self):
        """PropertySchema instantiation testing to confirm dict behavior."""
        schema_property = PropertySchema({'type': 'int', 'required': True})
        self.assertIsNotNone(schema_property)

        schema_property = PropertySchema({'type': 'int', 'required': False})
        self.assertIsNotNone(schema_property)


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