"""Test the basic functionality of the base and core data types."""
from ook import object_type
from test.test_utils import base_test_case


class ObjectTypeTest(base_test_case.BaseTestCase):
    """ObjectType test cases."""

    def test_dynamic_access(self):
        """ObjectType property access as a Dict and an Attribute."""
        some_type = object_type.ObjectType()
        self.assert_dynamic_accessing(some_type)
