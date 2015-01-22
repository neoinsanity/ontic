from test.test_utils import base_test_case

from ontic.meta_type import MetaType


class MetaTypeTest(base_test_case.BaseTestCase):
    """MetaType test cases"""

    def test_meta_type_instantiation(self):
        """MetaType instantiation testing to confirm dict behavior."""
        meta_object = MetaType()
        self.assertIsNotNone(meta_object)

        meta_object = MetaType({'prop1': 'val1', 'prop2': 'val2'})
        self.assertIsNotNone(meta_object)
        self.assertEqual('val1', meta_object['prop1'])
        self.assertEqual('val2', meta_object.prop2)

        meta_object = MetaType(prop1='val1', prop2='val2')
        self.assertIsNotNone(meta_object)
        self.assertEqual('val1', meta_object['prop1'])
        self.assertEqual('val2', meta_object.prop2)

        meta_object = MetaType([['prop1', 'val1'], ['prop2', 'val2']])
        self.assertIsNotNone(meta_object)
        self.assertEqual('val1', meta_object['prop1'])
        self.assertEqual('val2', meta_object.prop2)

    def test_meta_type_dynamic_access(self):
        """MetaType property access as a Dict and an Attribute."""
        meta_object = MetaType()
        self.assert_dynamic_accessing(meta_object)
