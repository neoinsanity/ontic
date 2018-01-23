"""An exception to signal a validation failure."""


class ValidationException(Exception):
    """Exception used to signal validation errors."""

    def __init__(self, validation_errors=None):
        """

        :param validation_errors: A list of validation failures that are
            triggering the *ValidationException*.
        :type validation_errors: list<str>
        """
        self._validation_errors = validation_errors if validation_errors else []
        message = str.join(' \n', validation_errors)
        super(ValidationException, self).__init__(message)

    @property
    def validation_errors(self):
        """List of validation errors that triggered the *ValidationException*.

        :return: A list of the validation errors encountered.
        :rtype: list<str>
        """

        return self._validation_errors
