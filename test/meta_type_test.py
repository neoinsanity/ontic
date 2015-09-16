from test.test_utils import base_test_case

from ontic.meta_schema_type import MetaSchemaType


class MetaSchemaTypeTest(base_test_case.BaseTestCase):
    """MetaSchemaType test cases"""

    def test_meta_type_instantiation(self):
        """MetaSchemaType instantiation testing to confirm dict behavior."""
        meta_object = MetaSchemaType()
        self.assertIsNotNone(meta_object)

        meta_object = MetaSchemaType({'prop1': 'val1', 'prop2': 'val2'})
        self.assertIsNotNone(meta_object)
        self.assertEqual('val1', meta_object['prop1'])
        self.assertEqual('val2', meta_object.prop2)

        meta_object = MetaSchemaType(prop1='val1', prop2='val2')
        self.assertIsNotNone(meta_object)
        self.assertEqual('val1', meta_object['prop1'])
        self.assertEqual('val2', meta_object.prop2)

        meta_object = MetaSchemaType([['prop1', 'val1'], ['prop2', 'val2']])
        self.assertIsNotNone(meta_object)
        self.assertEqual('val1', meta_object['prop1'])
        self.assertEqual('val2', meta_object.prop2)

    def test_meta_type_dynamic_access(self):
        """MetaSchemaType property access as a Dict and an Attribute."""
        meta_object = MetaSchemaType()
        self.assert_dynamic_accessing(meta_object)
