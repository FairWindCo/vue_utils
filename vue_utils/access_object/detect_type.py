import sys

if sys.version_info < (3, 7, 0):
    from collections import Sequence
    from collections.abc import Mapping
else:
    from collections.abc import Sequence
    from collections import Mapping

primitiveTypes = (int, float, bool, str)


def is_primitive(obj):
    return isinstance(obj, primitiveTypes)


def is_sequence(obj):
    return isinstance(obj, Sequence) or hasattr(obj, '__iter__')


def is_not_string_sequence(obj):
    return not isinstance(obj, str) and is_sequence(obj)


def is_dict(obj):
    return isinstance(obj, Mapping)
