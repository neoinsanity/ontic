import unittest


class BaseTestCase(unittest.TestCase):
    def assert_dynamic_accessing(self, ook_object):
        # Assignment by attribute
        ook_object.attr1 = 1
        self.assertEqual(1, ook_object.attr1)
        self.assertEqual(1, ook_object['attr1'])
        ook_object.attr2 = 'Some string'
        self.assertEqual('Some string', ook_object.attr2)
        self.assertEqual('Some string', ook_object['attr2'])

        # Assignment by key
        ook_object['key1'] = 3
        self.assertEqual(3, ook_object['key1'], 3)
        self.assertEqual(3, ook_object.key1)
        ook_object['key2'] = 'Some value'
        self.assertEqual('Some value', ook_object['key2'])
        self.assertEqual('Some value', ook_object.key2)

        # Retrieval failures follow expected interface behavior
        self.assertRaises(AttributeError, getattr, ook_object, 'no_attribute')
        self.assertRaises(KeyError, lambda: ook_object['bad_key'])

        self.assertDictEqual(dict(), ook_object.get_schema())
