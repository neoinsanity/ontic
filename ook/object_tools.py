import re

from object_type import BaseType

type_map = {
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'list': list,
    'set': set,
    'str': basestring,
}

collection_set = {dict, list, set}


def validate_object(the_object):
    """

    :param the_object: An object instance whose type is a child class of
        `ook.object.BaseType`
    :type the_object: ook.object_type.BaseType

    """

    if not isinstance(the_object, BaseType):
        raise ValueError('Validation can only support validation of objects '
                         'derived from ook.BaseType')

    value_errors = []

    for key, metadata in the_object.get_schema().iteritems():
        value = the_object.get(key, None)
        value_type = type_map.get(metadata.get('type', None), None)
        item_type = type_map.get(metadata.get('item_type', None), None)

        # required: True | False
        if metadata.get('required', False) and value is None:
            value_errors.append('The value for "%s" is required.' % key)

        # check if there is a value_type to continue processing
        if value_type and value is not None:
            # type checking
            if not isinstance(value, value_type):
                value_errors.append(
                    'The value for "%s" is not of type "%s": %s' %
                    (key, metadata.type, str(value)))
                continue  # don't assume successful testing based on value_type

            #todo: raul - split this up into collection and single validation.
            _validate_value(key, metadata, value_type, value, value_errors)

    if value_errors:
        raise ValueError(str.join(' \n-- ', value_errors))


def _validate_value(key, metadata, value_type, value, value_errors):
    # min
    if hasattr(metadata, 'min'):
        if ((value_type is basestring or value_type in collection_set)
            and len(value) < metadata.min):
            value_errors.append(
                'The value for "%s" fails the minimum length of %s' %
                (key, metadata.min))

    # max
    if hasattr(metadata, 'max'):
        if ((value_type is basestring or value_type in collection_set)
            and len(value) < metadata.max):
            value_errors.append(
                'The value for "%s" fails the maximum length of %s' %
                (key, metadata.max))

    # regex validation
    if hasattr(metadata, 'regex'):
        if value_type is basestring and value is not '':
            if not re.match(metadata.regex, value):
                value_errors.append(
                    'Value for %s does not meet regex: %s' %
                    (key, metadata.regex))
        if value_type in {list, set}:
            for item_value in value:
                if not re.match(metadata.regex, item_value):
                    value_errors.append(
                        'Value %s in %s does not meet regex: %s' %
                        (item_value, key, metadata))

