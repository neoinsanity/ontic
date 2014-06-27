"""

"""


class ValidationException(Exception):
    def __init__(self, validation_errors=[]):
        self._validation_errors = validation_errors
        message = str.join(' \n', validation_errors)
        super(ValidationException, self).__init__(message)

    @property
    def validation_errors(self):
        return self._validation_errors
