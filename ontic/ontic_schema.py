"""

"""
from typing import List

from ontic import ontic_meta
from ontic import ontic_property
from ontic.validation_exception import ValidationException


class OnticSchema(ontic_meta.OnticMeta):
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
            if not isinstance(value, ontic_property.OnticProperty):
                self[key] = ontic_property.OnticProperty(value)

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

    [property_schema.perfect() for property_schema in ontic_schema.values()]


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
    for prop in ontic_schema.values():
        value_errors.extend(
            prop.validate(raise_validation_exception=False))

    if value_errors and raise_validation_exception:
        raise ValidationException(value_errors)

    return value_errors
