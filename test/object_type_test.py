"""Test the basic functionality of the base and core data types."""
from ontic import ontic_type
from test.test_utils import base_test_case


class OnticTypeTest(base_test_case.BaseTestCase):
    """OnticType test cases."""

    def test_object_type_instantiation(self):
        """OnticType instantiation to confirm dict behavior"""
        schema = {'prop': {'type': 'int'}}
        my_type = ontic_type.create_ontic_type('MyType', schema)

        expected_dict = {'prop': 3}

        my_object = my_type()
        my_object.prop = 3
        self.assertDictEqual(expected_dict, my_object)

    def test_dynamic_access(self):
        """OnticType property access as a Dict and an Attribute."""
        some_type = ontic_type.OnticType()
        self.assert_dynamic_accessing(some_type)
