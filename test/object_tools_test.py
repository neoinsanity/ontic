import base_test_case

from ook import object_tools
from ook.object_type import BaseType


class TestType(BaseType):
    pass


class ObjectToolsCreateOokTypeTest(base_test_case.BaseTestCase):
    """Test the dynamic creation of Ook types."""

    def test_create_ook_type_arg_errors(self):
        """Assert the create ook type arg errors."""
        self.assertRaises(
            ValueError, object_tools.create_ook_type, name=None, schema=dict())
        self.assertRaises(
            ValueError, object_tools.create_ook_type, name='SomeName', schema=None)
        self.assertRaises(
            ValueError, object_tools.create_ook_type, name='SomeName', schema=list())

    def test_create_ook_type(self):
        """The most simple and basic dynamic Ook."""
        ook_type = object_tools.create_ook_type('Barebone', dict())

        self.assertIsNotNone(ook_type)

        ook_object = ook_type()
        self.assert_dynamic_accessing(ook_object)
        self.assertIsInstance(ook_object, ook_type)


class PropertySchemaTest(base_test_case.BaseTestCase):
    def test_type_setting(self):
        schema = {
            'bool_property': {'type': 'bool'},
            'dict_property': {'type': 'dict'},
            'float_property': {'type': 'float'},
            'int_property': {'type': 'int'},
            'list_property': {'type': 'list'},
            'set_property': {'type': 'set'},
            'str_property': {'type': 'str'}
        }

        # Create the type
        ook_type = object_tools.create_ook_type('Typer', schema)
        self.assertIsNotNone(ook_type)

        # Create object of type
        ook_object = ook_type()
        self.assertIsInstance(ook_object, ook_type)
        self.assertDictEqual(schema, ook_type.get_schema())

        # Validate an empty object.
        object_tools.validate_object(ook_object)

        # Validate with known good data.
        ook_object.bool_property = True
        ook_object.dict_property = {'some_key': 'some_value'}
        ook_object.float_property = 3.4
        ook_object.int_property = 5
        ook_object.list_property = [5, 6, 7]
        ook_object.set_property = {'dog', 'cat', 'mouse'}
        ook_object.str_property = 'some_string'
        object_tools.validate_object(ook_object)

        # Validate with known bad type.
        ook_object.bool_property = 'Dog'
        self.assertRaises(ValueError, object_tools.validate_object, ook_object)


class ObjectToolsTest(base_test_case.BaseTestCase):
    def _test_email_template_validation(self):
        """General EmailTemplate validation suite."""

        # No key value error.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': None,
                              'description': 'This is a good email template.',
                              'to': {'someone@xcorp.com', 'manager@xcorp.com'},
                              'cc': {'coworker@xcorp.com'},
                              'subject': 'The subject line for the email.',
                              'body': 'A body of good text for our good email.',
                          }))

        # Invalid type.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': 32,
                              'description': 'This is a good email template.',
                              'to': {'someone@xcorp.com', 'manager@xcorp.com'},
                              'cc': {'coworker@xcorp.com'},
                              'subject': 'The subject line for the email.',
                              'body': 'A body of good text for our good email.',
                          }))

        # Minimal key length value error.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': '',
                              'description': 'This is a good email template.',
                              'to': {'someone@xcorp.com', 'manager@xcorp.com'},
                              'cc': {'coworker@xcorp.com'},
                              'subject': 'The subject line for the email.',
                              'body': 'A body of good text for our good email.',
                          }))

        # Maximum key length value error.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': 'AVeryBigKeyThatWillFail',
                              'description': 'This is a good email template.',
                              'to': {'someone@xcorp.com', 'manager@xcorp.com'},
                              'cc': {'coworker@xcorp.com'},
                              'subject': 'The subject line for the email.',
                              'body': 'A body of good text for our good email.',
                          }))

        # Value not alphanumeric, period, or dash only characters value error.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': 'No/Slash',
                              'description': 'This is a good email template.',
                              'to': {'someone@xcorp.com', 'manager@xcorp.com'},
                              'cc': {'coworker@xcorp.com'},
                              'subject': 'The subject line for the email.',
                              'body': 'A body of good text for our good email.',
                          }))

        # Description greater than 1024 chars value error.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': '10-Valid.Key',
                              'description': 'x' * 1025,
                              'to': {'someone@xcorp.com', 'manager@xcorp.com'},
                              'cc': {'coworker@xcorp.com'},
                              'subject': 'The subject line for the email.',
                              'body': 'A body of good text for our good email.',
                          }))  # No to value error.

        # Minimum to length value error.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': '10-Valid.Key',
                              'description': 'This is a good email template.',
                              'to': set(),
                              'cc': {'coworker@xcorp.com'},
                              'subject': 'The subject line for the email.',
                              'body': 'A body of good text for our good email.',
                          }))  # No to value error.


        # Invalid email address in to value error.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': '10-Valid.Key',
                              'description': 'This is a good email template.',
                              'to': {'someone@xcorp.com', 'bad.com'},
                              'cc': {'coworker@xcorp.com'},
                              'subject': 'The subject line for the email.',
                              'body': 'A body of good text for our good email.',
                          }))  # No to value error.

        # Invalid email address in cc value error.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': '10-Valid.Key',
                              'description': 'This is a good email template.',
                              'to': {'someone@xcorp.com', 'manager@xcorp.com'},
                              'cc': {'bad.com'},
                              'subject': 'The subject line for the email.',
                              'body': 'A body of good text for our good email.',
                          }))  # No to value error.

        # No subject value error.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': '10-Valid.Key',
                              'description': 'This is a good email template.',
                              'to': {'someone@xcorp.com', 'manager@xcorp.com'},
                              'cc': {'coworker@xcorp.com'},
                              'subject': None,
                              'body': 'A body of good text for our good email.',
                          }))  # No to value error.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': '10-Valid.Key',
                              'description': 'This is a good email template.',
                              'to': {'someone@xcorp.com', 'manager@xcorp.com'},
                              'cc': {'coworker@xcorp.com'},
                              'subject': '',
                              'body': 'A body of good text for our good email.',
                          }))  # No to value error.

        # No body value error.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': '10-Valid.Key',
                              'description': 'This is a good email template.',
                              'to': {'someone@xcorp.com', 'manager@xcorp.com'},
                              'cc': {'coworker@xcorp.com'},
                              'subject': 'The subject line for the email.',
                              'body': '',
                          }))  # No to value error.
        self.assertRaises(ValueError, object_tools.validate_object,
                          TestType({
                              'key': '10-Valid.Key',
                              'description': 'This is a good email template.',
                              'to': {'someone@xcorp.com', 'manager@xcorp.com'},
                              'cc': {'coworker@xcorp.com'},
                              'subject': 'The subject line for the email.',
                              'body': None,
                          }))  # No to value error.

        # This is the completely valid example.
        good_data = TestType({
            'key': '10.Email-Tmpl',
            'description': 'This is a good email template.',
            'to': {'someone@xcorp.com', 'manager@xcorp.com'},
            'cc': {'coworker@xcorp.com'},
            'subject': 'The subject line for the email.',
            'body': 'A body of good text for our good email.',
        })

        try:
            object_tools.validate_object(good_data)
        except:
            self.assertFalse(True, 'This call should have succeeded.')
