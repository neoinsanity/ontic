"""

"""
from typing import List, Union

from ontic.ontic_core import OnticCore
from ontic.validation_exception import ValidationException


class SchemaInterface(OnticCore):
    ONTIC_SCHEMA = None

    @classmethod
    def get_schema(cls) -> 'OnticSchema':
        return cls.ONTIC_SCHEMA

    @classmethod
    def __set_schema_for_ontic_schema__(
            cls, ontic_schema: Union['OnticSchema', dict]) -> None:
        cls.ONTIC_SCHEMA = OnticSchema(ontic_schema)


class OnticProperty(SchemaInterface):
    """A class to define a schema for a property."""

    def perfect(self) -> None:
        """Method to ensure the completeness of a given schema property.

        :rtype: None
        :raises ValueError: If the candidate_property_type is None, or not
            of type *PropertyType*.
        """
        perfect_property(self)

    def validate(self, raise_validation_exception: bool = True) -> None:
        """Method to validate a property schema definition.

        :param raise_validation_exception: If True, then
            *validate_property_type* will throw a *ValueException* upon
            validation failure. If False, then a list of validation errors is
            returned. Defaults to True.
        :type raise_validation_exception: bool
        :return: If no validation errors are found, then *None* is returned.
            If validation fails, then a list of the errors is returned if the
            *raise_validation_exception* is set to True.
        :rtype: list<str>, None
        :raises ValueError: *the_candidate_schema_property* is not an
            :class:`OnticProperty`.
        :raises ValidationException: A property of *candidate_property_type*
            does not meet schema requirements.
        """
        return validate_property(self, raise_validation_exception)


def perfect_property(ontic_property: OnticProperty) -> None:
    """Method to ensure the completeness of a given schema property.

    This method ensures completeness by stripping out any properties that
    are not defined by the schema definition. In addition, for any schema
    properties that are not included, the method will add those
    properties to the default value.

    :param ontic_property: The OnticProperty that is to be clean and restricted.
    :type ontic_property: :class:`OnticProperty`
    :rtype: None
    :raises ValueError: If the ontic_property is None, or not of type
        *OnticProperty*.
    """
    if ontic_property is None:
        raise ValueError('"ontic_property" must be provided.')
    if not isinstance(ontic_property, OnticProperty):
        raise ValueError('"ontic_property" must be OnticProperty type.')

    property_schema = ontic_property.get_schema()

    # remove un-necessary properties.
    extra_properties = set(ontic_property.keys()) - set(property_schema.keys())
    for property_name in extra_properties:
        del ontic_property[property_name]

    if 'type' in ontic_property:
        _perfect_type_setting(ontic_property)
    else:
        ontic_property.type = None

    if 'member_type' in ontic_property:
        # coerce member_type declarations as string to base types.
        ontic_property.member_type = TYPE_MAP[ontic_property.member_type]
    else:
        ontic_property.member_type = None

    # set the default for the given property.
    for property_name, property_schema in property_schema.items():
        if property_name not in ontic_property:
            ontic_property[property_name] = None
        if ontic_property[property_name] is None:
            ontic_property[property_name] = property_schema.default


def validate_property(
        ontic_property: OnticProperty,
        raise_validation_exception: bool = True) -> List[str]:
    """Method to validate a property schema definition.

    :param candidate_property_type: The schema property to be validated.
    :type candidate_property_type: :class:`property_type.PropertyType`
    :param raise_validation_exception: If True, then *validate_property_type*
        will throw a *ValueException* upon validation failure. If False,
        then a list of validation errors is returned. Defaults to True.
    :type raise_validation_exception: bool
    :return: If no validation errors are found, then *None* is
        returned. If validation fails, then a list of the errors is returned
        if the *raise_validation_exception* is set to True.
    :rtype: list<str>, None
    :raises ValueError: *the_candidate_schema_property* is not an
        :class:`~ontic.ontic_type.OnticType`.
    :raises ValidationException: A property of *candidate_property_type*
        does not meet schema requirements.
    """
    if ontic_property is None:
        raise ValueError('"ontic_property" must be provided.')
    if not isinstance(ontic_property, OnticProperty):
        raise ValueError('"ontic_property" must be OnticProperty type.')

    value_errors = []

    for setting_name, setting_schema in ontic_property.get_schema().items():
        setting_value = ontic_property.get(setting_name, None)

        # todo: raul - for now skip validating compound schemas.
        if (isinstance(setting_value, type) and
                issubclass(setting_value, SchemaInterface)):
            continue

        value_errors.extend(
            validate_value(setting_name, setting_schema, setting_value))

    if value_errors and raise_validation_exception:
        raise ValidationException(value_errors)

    return value_errors


class OnticSchema(SchemaInterface):
    """The type definition for a schema object.

    The **OnticSchema** contains a dictionary of property field names and
    the corresponding **OnticProperty** definition.

    Example OnticSchema representation::

        OnticSchema({
          'some_property': OnticSchema({
                'type': 'str',
                'required': True
            })
        })

    For a complete list of :class:`OnticProperty` settings, see
    :ref:`property-schema-settings-table`.
    """

    def __init__(self, *args, **kwargs):
        super(OnticSchema, self).__init__(*args, **kwargs)
        for key, value in self.items():
            if not isinstance(value, OnticProperty):
                self[key] = OnticProperty(value)

    def perfect(self) -> None:
        """Method to clean and perfect a given schema.

        The *perfect* will fill in any missing schema settings for each of
        the :class:`OnticProperty`. This function should be used to ensure
        property schema completeness.

        :rtype: None
        """
        perfect_schema(self)

    def validate(self, raise_validation_exception: bool = True) -> List[str]:
        """Validate a given :class:`OnticSchema`.

        This method will iterate through all of the
        :class:`OnticProperty` and validate that each definition is valid.
        The method will collect all of the errors and return those as a list
        of strings or raise a
        :class:`ontic.validation_exception.ValidationException`. The switch in
        behavior is determined by the *raise_validation_exception*

        :param raise_validation_exception: If True, then *validate_schema* will
            throw a *ValidationException* upon validation failure. If False,
            then a list of validation errors is returned. Defaults to True.
        :type raise_validation_exception: bool
        :return: List of errors found. Empty of no errors found.
        :rtype: list<str>
        :raises ValueError: *candidate_schema* is None, or not of type
            :class:`SchemaType`.
        :raises ValidationException: A property of *candidate_schema* does not
            meet schema requirements.
        """
        return validate_schema(self, raise_validation_exception)


def perfect_schema(ontic_schema: OnticSchema) -> None:
    """Method to clean and perfect a given schema.

    The *perfect_schema* will fill in any missing schema setting for each of
    the :class:`OnticProperty`. This function should be used to ensure
    property schema completeness.

    :param ontic_schema: The schema that is to be perfected.
    :type ontic_schema: :class:`OnticSchema`
    :rtype: None
    """
    if ontic_schema is None:
        raise ValueError('"ontic_schema" must be provided.')
    if not isinstance(ontic_schema, OnticSchema):
        raise ValueError('"ontic_schema" argument must be of OnticSchema type.')

    [ontic_property.perfect() for ontic_property in ontic_schema.properties]


def validate_schema(
        ontic_schema: OnticSchema,
        raise_validation_exception: bool = True) -> List[str]:
    """Validate a given :class:`OnticSchema`.

    This method will iterate through all of the :class:`OnticProperty` and
    validate that each definition is valid.  The method will collect all of
    the errors and return those as a list of strings or raise a
    :class:`ontic.validation_exception.ValidationException`. The switch in
    behavior is determined by the *raise_validation_exception*

    :param ontic_schema: The schema to be validated.
    :type ontic_schema: :class:`OnticSchema`
    :param raise_validation_exception: If True, then *validate_schema* will
        throw a *ValidationException* upon validation failure. If False, then a
        list of validation errors is returned. Defaults to True.
    :type raise_validation_exception: bool
    :return: List of errors found. Empty of no errors found.
    :rtype: list<str>
    :raises ValueError: *ontic_schema* is None, or not of type
        :class:`OnticSchema`.
    :raises ValidationException: A property of *ontic_schema* does not
        meet schema requirements.
    """
    if ontic_schema is None:
        raise ValueError('"ontic_schema" argument must be provided.')
    if not isinstance(ontic_schema, OnticSchema):
        raise ValueError('"ontic_schema" argument must be of OnticSchema type.')

    value_errors = []
    for ontic_property in ontic_schema.properties:
        value_errors.extend(
            ontic_property.validate(raise_validation_exception=False))

    if value_errors and raise_validation_exception:
        raise ValidationException(value_errors)

    return value_errors


__ONTIC_SCHEMA_BOOTSTRAP_SCHEMA__ = OnticSchema(
    properties=OnticProperty(
        type=list,
        required=True
    )
)

__ONTIC_PROPERTY_BOOTSTRAP_SCHEMA__ = OnticSchema({
    'type': OnticProperty({
        'type': (str, type),
        'default': None,
        'required': False,
        'enum': TYPE_SET + (None,),
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'default': OnticProperty({
        'type': None,
        'default': None,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'required': OnticProperty({
        'type': bool,
        'default': False,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'enum': OnticProperty({
        'type': set,
        'default': None,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'min': OnticProperty({
        'type': tuple(COMPARABLE_TYPES),
        'default': None,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'max': OnticProperty({
        'type': tuple(COMPARABLE_TYPES),
        'default': None,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'regex': OnticProperty({
        'type': str,
        'default': None,
        'required': False,
        'enum': None,
        'min': 1,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'member_type': OnticProperty({
        'type': (str, type),
        'default': None,
        'required': False,
        'enum': TYPE_SET + (None,),
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'member_min': OnticProperty({
        'type': tuple(COMPARABLE_TYPES),
        'default': None,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
    'member_max': OnticProperty({
        'type': tuple(COMPARABLE_TYPES),
        'default': None,
        'required': False,
        'enum': None,
        'min': None,
        'max': None,
        'regex': None,
        'member_type': None,
        'member_min': None,
        'member_max': None,
    }),
})

# Bootstrap OnticSchema class with a schema definition.
OnticSchema.__set_schema_for_ontic_schema__(
    __ONTIC_SCHEMA_BOOTSTRAP_SCHEMA__)

# Bootstrap OnticPropeerty class with a schema defintion.
OnticProperty.__set_schema_for_ontic_schema__(
    __ONTIC_PROPERTY_BOOTSTRAP_SCHEMA__)
