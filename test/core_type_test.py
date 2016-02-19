"""Test the basic functionality of the core and meta data types."""

from copy import copy, deepcopy

from test.test_utils import base_test_case
from ontic.core_type import CoreType


class CoreTypeTest(base_test_case.BaseTestCase):
    """CoreType test cases."""

    def test_core_type_instantiation(self):
        """CoreType instantiation testing to confirm dict behavior."""
        core_object = CoreType()
        self.assertIsNotNone(core_object)

        core_object = CoreType({'prop1': 'val1', 'prop2': 'val2'})
        self.assertIsNotNone(core_object)
        self.assertEqual('val1', core_object['prop1'])
        self.assertEqual('val2', core_object.prop2)

        core_object = CoreType(prop1='val1', prop2='val2')
        self.assertIsNotNone(core_object)
        self.assertEqual('val1', core_object['prop1'])
        self.assertEqual('val2', core_object.prop2)

        core_object = CoreType([['prop1', 'val1'], ['prop2', 'val2']])
        self.assertIsNotNone(core_object)
        self.assertEqual('val1', core_object['prop1'])
        self.assertEqual('val2', core_object.prop2)

    def test_core_type_dynamic_access(self):
        """CoreType property access as a Dict and an Attribute."""
        core_object = CoreType()
        self.assert_dynamic_accessing(core_object)

    def test_core_type_copy(self):
        """Ensure that CoreType supports copy operation."""

        class SubType(CoreType):
            pass

        sub_object = SubType(
            int_prop=1,
            str_prop='dog',
            list_prop=[2, 'cat'],
            dict_prop={
                'int_key': 3,
                'str_key': 'mouse',
                'list_key': [4, 'fish'],
                'dict_key': {'key1': 'red',
                             'key2': 'blue',
                             'key3': 'green'}
            }
        )

        sub_copy = copy(sub_object)

        self.assertIsInstance(sub_copy, SubType)
        self.assertIsNot(sub_object, sub_copy)
        self.assertDictEqual(sub_object, sub_copy)
        self.assertIs(sub_copy.int_prop, sub_object.int_prop)
        self.assertIs(sub_copy.str_prop, sub_object.str_prop)
        self.assertIs(sub_copy.list_prop, sub_object.list_prop)
        self.assertIs(sub_copy.dict_prop, sub_object.dict_prop)

    def test_core_type_deepcopy(self):
        """Ensure that CoreType supports deepcopy operation."""

        class SubType(CoreType):
            pass

        sub_object = SubType(
            int_prop=1,
            str_prop='dog',
            list_prop=[2, 'cat'],
            dict_prop={
                'int_key': 3,
                'str_key': 'mouse',
                'list_key': [4, 'fish'],
                'dict_key': {'key1': 'red',
                             'key2': 'blue',
                             'key3': 'green'}
            }
        )

        sub_copy = deepcopy(sub_object)

        self.assertIsInstance(sub_copy, SubType)
        self.assertIsNot(sub_object, sub_copy)
        self.assertDictEqual(sub_object, sub_copy)
        self.assertIs(sub_copy.int_prop, sub_object.int_prop)
        self.assertIs(sub_copy.str_prop, sub_object.str_prop)
        self.assertIsNot(sub_copy.list_prop, sub_object.list_prop)
        self.assertIsNot(sub_copy.dict_prop, sub_object.dict_prop)
        self.assertIsNot(sub_copy.dict_prop['list_key'],
                         sub_object.dict_prop['list_key'])


