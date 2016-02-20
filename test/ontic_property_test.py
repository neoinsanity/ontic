"""OnticProperty unit tests."""
from copy import copy, deepcopy

from ontic.ontic_property import OnticProperty

from test.utils import BaseTestCase


class OnticMetaTest(BaseTestCase):
    """OnticProperty test cases."""

    def test_ontic_property_instantiation(self):
        """OnticProperty instantiation testing to confirm dict behaviour."""
        ontic_property1 = OnticProperty()
        self.assertIsNotNone(ontic_property1)

        # Test dictionary initialization.
        ontic_property2 = OnticProperty(
            {
                'type': int,
                'default': 1,
                'required': True
            }
        )
        self.assertIsNotNone(ontic_property2)
        self.assertEqual(int, ontic_property2['type'])
        self.assertEqual(1, ontic_property2.default)
        self.assertEqual(True, ontic_property2['required'])

        # Test initialization by property.
        ontic_property3 = OnticProperty(
            type=int,
            default=1,
            required=True)
        self.assertIsNotNone(ontic_property3)
        self.assertEqual(int, ontic_property3.type)
        self.assertEqual(1, ontic_property3['default'])
        self.assertEqual(True, ontic_property3.required)

        # Test initialization by list.
        ontic_property4 = OnticProperty(
            [['type', int],['default', 1],['required', True]])
        self.assertIsNotNone(ontic_property4)
        self.assertEqual(int, ontic_property4['type'])
        self.assertEqual(1, ontic_property4.default)
        self.assertEqual(True, ontic_property4['required'])

    def test_dynamic_access(self):
        """Ensure OnticProperty property access as dict and attribute."""
        the_property = OnticProperty()
        self.assert_dynamic_accessing(the_property)

    def test_copy(self):
        """Ensure that OnticProperty supports copy operations."""

        # Create the test data.
        sub_object = SubType( alsdkjfasdlfkj  - TODO: convert this to an actual OnticProperty for testing.
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
