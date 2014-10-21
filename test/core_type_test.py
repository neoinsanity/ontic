"""Test the basic functionality of the core and meta data types."""

from copy import copy, deepcopy
from test_utils import base_test_case

from ontic import meta_type
from ontic.meta_type import CoreType, MetaType, PropertySchema
from ontic.validation_exception import ValidationException


class CoreTypeTest(base_test_case.BaseTestCase):
    """CoreType test cases."""

    def test_core_type_instantiation(self):
        """CoreType instantiation testing to confirm dict behavior."""
        core_object = CoreType()
        self.assertIsNotNone(core_object)

        core_object = CoreType({'prop1': 'val1', 'prop2': 'val2'})
        self.assertIsNotNone(core_object)
        self.assertEqual('val1', core_object['prop1'])
        self.assertEqual('val2', core_object.prop2)

        core_object = CoreType(prop1='val1', prop2='val2')
        self.assertIsNotNone(core_object)
        self.assertEqual('val1', core_object['prop1'])
        self.assertEqual('val2', core_object.prop2)

        core_object = CoreType([['prop1', 'val1'], ['prop2', 'val2']])
        self.assertIsNotNone(core_object)
        self.assertEqual('val1', core_object['prop1'])
        self.assertEqual('val2', core_object.prop2)

    def test_core_type_dynamic_access(self):
        """CoreType property access as a Dict and an Attribute."""
        core_object = CoreType()
        self.assert_dynamic_accessing(core_object)

    def test_core_type_copy(self):
        """Ensure that CoreType supports copy operation."""

        class SubType(CoreType):
            pass

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

        sub_copy = copy(sub_object)

        self.assertIsInstance(sub_copy, SubType)
        self.assertIsNot(sub_object, sub_copy)
        self.assertDictEqual(sub_object, sub_copy)
        self.assertIs(sub_copy.int_prop, sub_object.int_prop)
        self.assertIs(sub_copy.str_prop, sub_object.str_prop)
        self.assertIs(sub_copy.list_prop, sub_object.list_prop)
        self.assertIs(sub_copy.dict_prop, sub_object.dict_prop)

    def test_core_type_deepcopy(self):
        """Ensure that CoreType supports deepcopy operation."""

        class SubType(CoreType):
            pass

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

        sub_copy = deepcopy(sub_object)

        self.assertIsInstance(sub_copy, SubType)
        self.assertIsNot(sub_object, sub_copy)
        self.assertDictEqual(sub_object, sub_copy)
        self.assertIs(sub_copy.int_prop, sub_object.int_prop)
        self.assertIs(sub_copy.str_prop, sub_object.str_prop)
        self.assertIsNot(sub_copy.list_prop, sub_object.list_prop)
        self.assertIsNot(sub_copy.dict_prop, sub_object.dict_prop)
        self.assertIsNot(sub_copy.dict_prop['list_key'],
                         sub_object.dict_prop['list_key'])


class MetaTypeTest(base_test_case.BaseTestCase):
    """MetaType test cases"""

    def test_meta_type_instantiation(self):
        """MetaType instantiation testing to confirm dict behavior."""
        meta_object = MetaType()
        self.assertIsNotNone(meta_object)

        meta_object = MetaType({'prop1': 'val1', 'prop2': 'val2'})
        self.assertIsNotNone(meta_object)
        self.assertEqual('val1', meta_object['prop1'])
        self.assertEqual('val2', meta_object.prop2)

        meta_object = MetaType(prop1='val1', prop2='val2')
        self.assertIsNotNone(meta_object)
        self.assertEqual('val1', meta_object['prop1'])
        self.assertEqual('val2', meta_object.prop2)

        meta_object = MetaType([['prop1', 'val1'], ['prop2', 'val2']])
        self.assertIsNotNone(meta_object)
        self.assertEqual('val1', meta_object['prop1'])
        self.assertEqual('val2', meta_object.prop2)

    def test_meta_type_dynamic_access(self):
        """MetaType property access as a Dict and an Attribute."""
        meta_object = MetaType()
        self.assert_dynamic_accessing(meta_object)


class PropertySchemaTest(base_test_case.BaseTestCase):
    """PropertySchema test cases"""

    def test_property_schema_instantiation(self):
        """PropertySchema instantiation testing to confirm dict behavior."""
        property_schema = PropertySchema()
        self.assertIsNotNone(property_schema)

        expected_schema = {
            'default': None,
            'enum': None,
            'max': 7,
            'member_max': None,
            'member_min': None,
            'member_type': None,
            'min': 3,
            'regex': None,
            'required': True,
            'type': int,
        }

        property_schema = PropertySchema({
            'type': 'int',
            'required': True,
            'min': 3,
            'max': 7,
        })
        self.assertIsNotNone(property_schema)
        self.assertDictEqual(expected_schema, property_schema)

        property_schema = PropertySchema(
            type='int', required=True, min=3, max=7)
        self.assertIsNotNone(property_schema)
        self.assertDictEqual(expected_schema, property_schema)

        property_schema = PropertySchema(
            [['type', 'int'], ['required', True], ['min', 3], ['max', 7]])
        self.assertIsNotNone(property_schema)
        self.assertDictEqual(expected_schema, property_schema)

    def test_property_schema_instantiation_failure(self):
        """Validate error reporting for bad PropertySchema definition."""

        bad_schema_test_case = {'type': 'UNDEFINED'}

        self.assertRaisesRegexp(
            ValueError,
            r"""Illegal type declaration: UNDEFINED""",
            PropertySchema, bad_schema_test_case)


class ValidateSchemaProperty(base_test_case.BaseTestCase):
    """Various tests of the 'validate_property_schema' method."""

    def test_bad_validate_schema_property_call(self):
        """Test bad use cases of validate_property_schema function call."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_property_schema" must be provided.',
            meta_type.validate_property_schema, None, list())

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_property_schema" must be PropertySchema type.',
            meta_type.validate_property_schema, dict(), list())

    def test_validate_schema_property_exception(self):
        """Test validate_schema validation exception handling."""
        invalid_property_schema = PropertySchema()
        invalid_property_schema.type = 'UNKNOWN'

        self.maxDiff = None
        self.assertRaisesRegexp(
            ValidationException,
            r"""The value "UNKNOWN" for "type" not in enumeration \[.*\].""",
            meta_type.validate_property_schema, invalid_property_schema)

        value_errors = meta_type.validate_property_schema(
            invalid_property_schema,
            raise_validation_exception=False)
        self.assertEqual(1, len(value_errors))
        self.assertTrue(value_errors[0].startswith(
            'The value "UNKNOWN" for "type" not in enumeration'))
