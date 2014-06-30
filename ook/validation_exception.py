"""An exception to signal a validation failure."""


class ValidationException(Exception):
    def __init__(self, validation_errors=list()):
        """

        :param validation_errors: A list of validation failures that are
            triggering the *ValidationException*.
        :type validation_errors: list<str>
        """
        self._validation_errors = validation_errors
        message = str.join(' \n', validation_errors)
        super(ValidationException, self).__init__(message)

    @property
    def validation_errors(self):
        """List of validation errors that triggered the *ValidationException*.

        :return: A list of the validation errors encountered.
        :rtype: list<str>
        """
        return self._validation_errors
