"""OnticMeta unit tests."""
from copy import copy, deepcopy

from test import utils

from ontic.ontic_meta import OnticMeta


class SubType(OnticMeta):
    """Sub-class of OnticMeta for testing purposes."""
    pass


class OnticMetaTest(utils.BaseTestCase):
    """OnticMeta test cases."""

    def test_ontic_meta_instantiation(self):
        """OnticMeta instantiation testing to confirm dict behaviour."""
        ontic_meta1 = OnticMeta()
        self.assertIsNotNone(ontic_meta1)

        # Test dictionary initialization.
        ontic_meta2 = OnticMeta({'prop1': 'val1', 'prop2': 'val2'})
        self.assertIsNotNone(ontic_meta2)
        self.assertEqual('val1', ontic_meta2['prop1'])
        self.assertEqual('val2', ontic_meta2.prop2)

        # Test initialization by property.
        ontic_meta3 = OnticMeta(prop1='val1', prop2='val2')
        self.assertIsNotNone(ontic_meta3)
        self.assertEqual('val1', ontic_meta3.prop1)
        self.assertEqual('val2', ontic_meta3['prop2'])

        # Test initialization by list.
        ontic_meta4 = OnticMeta([['prop1', 'val1'], ['prop2', 'val2']])
        self.assertIsNotNone(ontic_meta4)
        self.assertEqual('val1', ontic_meta4['prop1'])
        self.assertEqual('val2', ontic_meta4.prop2)

    def test_dynamic_access(self):
        """Ensure OnticMeta property access as dict and attribute."""
        ontic_meta = OnticMeta()
        self.assert_dynamic_accessing(ontic_meta)
        # Create the test data.

    def test_copy(self):
        """Ensure that OnticMeta supports copy operations."""

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
        """Ensure that OnticMeta supports deepcopy operation."""

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
