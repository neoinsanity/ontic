"""Test the basic functionality of the base and core data types."""
from ontic import object_type
from test.test_utils import base_test_case


class ObjectTypeTest(base_test_case.BaseTestCase):
    """ObjectType test cases."""

    def test_object_type_instantiation(self):
        """ObjectType instantiation to confirm dict behavior"""
        schema = {'prop': {'type': 'int'}}
        my_type = object_type.create_ontic_type('MyType', schema)

        expected_dict = {'prop': 3}

        my_object = my_type()
        my_object.prop = 3
        self.assertDictEqual(expected_dict, my_object)

    def test_dynamic_access(self):
        """ObjectType property access as a Dict and an Attribute."""
        some_type = object_type.ObjectType()
        self.assert_dynamic_accessing(some_type)
