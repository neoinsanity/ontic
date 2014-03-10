
import base_test_case
from ook import object_type


class BaseTypeTest(base_test_case.BaseTestCase):
    def test_dynamic_access(self):
        """BaseType property access as a Dict and an Attribute."""
        base_object = object_type.BaseType()
        self.assert_dynamic_accessing(base_object)
