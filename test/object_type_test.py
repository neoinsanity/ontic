"""Test the basic functionality of the base and core data types."""
import base_test_case
from ook import object_type


class CoreTypeTest(base_test_case.BaseTestCase):
    """CoreType test cases."""

    def test_dynamic_access(self):
        """_CoreType property access as a Dict and an Attribute."""
        core_object = object_type._CoreType()
        self.assert_dynamic_accessing(core_object)


class BaseTypeTest(base_test_case.BaseTestCase):
    """BaseType test cases."""

    def test_dynamic_access(self):
        """BaseType property access as a Dict and an Attribute."""
        base_object = object_type.BaseType()
        self.assert_dynamic_accessing(base_object)
