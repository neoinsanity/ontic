"""

"""
from typing import List

from ontic import ontic_meta
from ontic import validation_exception


class OnticProperty(ontic_meta.OnticMeta):
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
        ontic_property.member_type = ontic_meta.TYPE_MAP[
            ontic_property.member_type]
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

    :param ontic_property: The schema property to be validated.
    :type ontic_property: :class:`OnticProperty`
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
                issubclass(setting_value, ontic_meta.OnticMeta)):
            continue

        value_errors.extend(
            ontic_meta.validate_value(
                setting_name, setting_schema, setting_value))

    if value_errors and raise_validation_exception:
        raise validation_exception.ValidationException(value_errors)

    return value_errors


def _perfect_type_setting(ontic_property: OnticProperty) -> None:
    """Perfect the type setting for a given candidate property schema."""
    if ontic_property.type is None:
        return

    candidate_type = ontic_property.type
    # coerce type declarations as string to base types.
    if isinstance(candidate_type, str):
        try:
            candidate_type = ontic_property.type = ontic_meta.TYPE_MAP[
                candidate_type]
        except KeyError:
            raise ValueError('Illegal type declaration: %s' %
                             ontic_property.type)

    # ensure that the type declaration is valid
    is_supported_type = candidate_type in ontic_meta.TYPE_SET
    is_meta_schema_type = issubclass(candidate_type, ontic_meta.OnticMeta)
    if not (is_supported_type or is_meta_schema_type):
        raise ValueError('Illegal type declaration: %s' % candidate_type)
