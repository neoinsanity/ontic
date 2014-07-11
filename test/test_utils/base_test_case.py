"""Utility test cases for testing Ontic."""
import unittest


class BaseTestCase(unittest.TestCase):
    """BaseTest case has methods to test Ontic features and functionality."""

    def assert_dynamic_accessing(self, ontic_object):
        """Assert that ontic_object exhibits dynamic property accessing.

        :param ontic_object: Ontic object to validate for dynamic access.
        :type ontic_object: ontic.meta_type.CoreType
        """
        # Assignment by attribute
        ontic_object.attr1 = 1
        self.assertEqual(1, ontic_object.attr1)
        self.assertEqual(1, ontic_object['attr1'])
        ontic_object.attr2 = 'Some string'
        self.assertEqual('Some string', ontic_object.attr2)
        self.assertEqual('Some string', ontic_object['attr2'])

        # Assignment by key
        ontic_object['key1'] = 3
        self.assertEqual(3, ontic_object['key1'], 3)
        self.assertEqual(3, ontic_object.key1)
        ontic_object['key2'] = 'Some value'
        self.assertEqual('Some value', ontic_object['key2'])
        self.assertEqual('Some value', ontic_object.key2)

        # Retrieval failures follow expected interface behavior
        self.assertRaises(AttributeError, getattr, ontic_object, 'no_attribute')
        self.assertRaises(KeyError, lambda: ontic_object['bad_key'])
