"""Test the basic functionality of the base and core data types."""
from ook import object_type
from test.test_utils import base_test_case


class BaseTypeTest(base_test_case.BaseTestCase):
    """BaseType test cases."""

    def test_dynamic_access(self):
        """BaseType property access as a Dict and an Attribute."""
        base_object = object_type.BaseType()
        self.assert_dynamic_accessing(base_object)
