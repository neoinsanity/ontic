"""Test the basic functionality of the core and meta data types."""

import base_test_case

from ook.meta_type import _CoreType, MetaType


class CoreTypeTest(base_test_case.BaseTestCase):
    """CoreType test cases."""

    def test_core_type_instantiation(self):
        """_CoreType instantiation testing to confirm dict behavior."""
        core_object = _CoreType()
        self.assertIsNotNone(core_object)

        core_object = _CoreType({'prop1': 'val1', 'prop2': 'val2'})
        self.assertIsNotNone(core_object)
        self.assertEqual('val1', core_object['prop1'])
        self.assertEqual('val2', core_object.prop2)

        core_object = _CoreType(prop1='val1', prop2='val2')
        self.assertIsNotNone(core_object)
        self.assertEqual('val1', core_object['prop1'])
        self.assertEqual('val2', core_object.prop2)

        core_object = _CoreType([['prop1', 'val1'], ['prop2', 'val2']])
        self.assertIsNotNone(core_object)
        self.assertEqual('val1', core_object['prop1'])
        self.assertEqual('val2', core_object.prop2)

    def test_core_type_dynamic_access(self):
        """_CoreType property access as a Dict and an Attribute."""
        core_object = _CoreType()
        self.assert_dynamic_accessing(core_object)

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
