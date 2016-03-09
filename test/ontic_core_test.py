"""OnticCore unit tests."""
from copy import copy, deepcopy

from test import utils

from ontic.ontic_core import Core


class SubType(Core):
    """Sub-class of Core for testing purposes."""
    pass


class OnticCoreTest(utils.BaseTestCase):
    """Core test cases."""

    def test_ontic_core_instantiation(self):
        """Core instantiation to confirm dict behavior."""
        ontic_core1 = Core()
        self.assertIsNotNone(ontic_core1)

        # Test dictionary initialization.
        ontic_core2 = Core({'prop1': 'val1', 'prop2': 'val2'})
        self.assertIsNotNone(ontic_core2)
        self.assertEqual('val1', ontic_core2['prop1'])
        self.assertEqual('val2', ontic_core2.prop2)

        # Test initialization by property.
        ontic_core3 = Core(prop1='val1', prop2='val2')
        self.assertIsNotNone(ontic_core3)
        self.assertEqual('val1', ontic_core3.prop1)
        self.assertEqual('val2', ontic_core3['prop2'])

        # Test initialization by list.
        ontic_core4 = Core([['prop1', 'val1'], ['prop2', 'val2']])
        self.assertIsNotNone(ontic_core4)
        self.assertEqual('val1', ontic_core4['prop1'])
        self.assertEqual('val2', ontic_core4.prop2)

    def test_dynamic_access(self):
        """Core property access as a dict and as attribute."""
        ontic_core = Core()
        self.assert_dynamic_accessing(ontic_core)

    def test_copy(self):
        """Ensure that Core supports copy operations."""

        # Create the test data.
        sub_object = SubType(
            int_prop=1,
            str_prop='dog',
            list_prop=[2, 'cat'],
            dict_prop={
                'int_key': 3,
                'str_key': 'mouse',
                'list_key': [4, 'fish'],
                'dict_key': {
                    'key1': 'red',
                    'key2': 'blue',
                    'key3': 'green'
                }
            }
        )

        # Execute the test.
        sub_copy = copy(sub_object)

        # Validate the test results.
        self.assertIsInstance(sub_copy, SubType)
        self.assertIsNot(sub_object, sub_copy)
        self.assertDictEqual(sub_object, sub_copy)
        self.assertIs(sub_copy.int_prop, sub_object.int_prop)
        self.assertIs(sub_copy.str_prop, sub_object.str_prop)
        self.assertIs(sub_copy.list_prop, sub_object.list_prop)
        self.assertIs(sub_copy.dict_prop, sub_object.dict_prop)

    def test_deepcopy(self):
        """Ensure that Core supports deepcopy operation."""

        # Create the test data.
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

        # Execute the test.
        sub_copy = deepcopy(sub_object)

        # Validate the test results.
        self.assertIsInstance(sub_copy, SubType)
        self.assertIsNot(sub_object, sub_copy)
        self.assertDictEqual(sub_object, sub_copy)
        self.assertIs(sub_copy.int_prop, sub_object.int_prop)
        self.assertIs(sub_copy.str_prop, sub_object.str_prop)
        self.assertIsNot(sub_copy.list_prop, sub_object.list_prop)
        self.assertIsNot(sub_copy.dict_prop, sub_object.dict_prop)
        self.assertIsNot(sub_copy.dict_prop['list_key'],
                         sub_object.dict_prop['list_key'])
