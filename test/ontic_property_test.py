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
        ontic_property = OnticProperty(
            type=str,
            required=False,
            enum=('dog', 'cat'),
        )

        # Execute the test.
        property_copy = copy(ontic_property)

        # Validate the test results.
        self.assertIsNot(ontic_property, property_copy)
        self.assertIs(ontic_property.type, property_copy.type)
        self.assertIs(ontic_property.required, property_copy.required)
        self.assertIs(ontic_property.enum, property_copy.enum)

    def test_deepcopy(self):
        """Ensure that OnticMeta supports deepcopy operation."""

        # Create the test data.
        ontic_property = OnticProperty(
            type=str,
            required=False,
            enum=('dog', 'cat'),
        )

        # Execute the test.
        property_copy = deepcopy(ontic_property)

        # Validate the test results.
        self.assertIsNot(ontic_property, property_copy)
        self.assertIs(ontic_property.type, property_copy.type)
        self.assertIs(ontic_property.required, property_copy.required)
        self.assertIs(ontic_property.enum, property_copy.enum)
