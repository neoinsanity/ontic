""""""
from copy import copy, deepcopy


class OnticCore(dict):
    def __init__(self, *args, **kwargs):
        super(OnticCore, self).__init__(*args, **kwargs)

        self.__dict__ = self

    def __copy__(self):
        return type(self)(copy(dict(self)))

    def __deepcopy__(self, memo):
        the_copy = dict(self.__dict__)
        return type(self)(deepcopy(the_copy, memo))
