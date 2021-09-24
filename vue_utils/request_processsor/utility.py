import json
from typing import Iterable, Any
from urllib.parse import unquote

from django.db.models import Manager

from vue_utils.access_object.detect_type import is_dict, is_not_string_sequence

DJANGO_OPERATORS = ['__exact', '__iexact', '__contains', '__icontains', '__in', '__gt', '__gte', '__lt',
                    '__lte', '__startswith', '__istartswith', '__endswith', '__iendswith', '__range',
                    '__date', '__yesr', '__iso_year', '__month', '__day', '__week', '__week_day',
                    '__iso_week_day', '__quarter', '__time', '__hour', '__minute', '__second', '__regex',
                    '__iregex']


def special_name_part(field_name):
    if field_name.find('__') > 1:
        for special_name in DJANGO_OPERATORS:
            if field_name.endswith(special_name):
                return True, field_name[:-len(special_name)]
    return False, field_name


def get_extended_filed(request, form_field_name):
    value, exist_in_request = get_from_request(request, form_field_name)
    if not exist_in_request:
        for sub_name in DJANGO_OPERATORS:
            value, exist_in_request = get_from_request(request, f'{form_field_name}{sub_name}')
            if exist_in_request:
                form_field_name = f'{form_field_name}{sub_name}'
                break
    return value, exist_in_request, form_field_name


def get_field_value(obj: any, field_name: str, default_val: any = None, can_call_function=True):
    if obj and field_name:
        if is_dict(obj):
            return obj.get(field_name, default_val)
        elif is_not_string_sequence(obj) and field_name.isnumeric():
            index = int(field_name)
            return default_val if len(obj) <= index else obj[index]
        elif hasattr(obj, field_name):
            val = getattr(obj, field_name)
            if can_call_function and callable(val) and not isinstance(val, Manager):
                val = val()
            return val
        else:
            return default_val
    else:
        return default_val


def get_field_value_ex(obj: any, field_name: str, default_val: any = None, can_call_function=True):
    if obj is None:
        return default_val
    if '__' in field_name:
        fields = field_name.split('__')
        if fields:
            val = obj
            for field in fields:
                val = get_field_value(val, field, default_val, can_call_function)
                if val is None:
                    break
            return val
        return default_val
    else:
        return get_field_value(obj, field_name, default_val, can_call_function)


def get_from_request(request, request_param_name: str, default_value: any = None, raise_exception: bool = False,
                     request_methods: Iterable[str] = ('GET', 'POST', 'body')) -> (Any, bool):
    if request is None:
        if raise_exception:
            raise ValueError('Request is None')
        else:
            return default_value, False
    if request_param_name:
        for method_name in request_methods:
            method = get_field_value(request, method_name, None)
            if method:
                if isinstance(method, bytes):
                    try:
                        method_str = method.decode('utf-8')
                        method = json.loads(method_str)
                    except Exception:
                        if raise_exception:
                            raise ValueError(f'No field {request_param_name} in request')
                        else:
                            return default_value, False
                if request_param_name in method:
                    value = method.get(request_param_name)
                    if method == 'GET':
                        value = unquote(value)
                    return value, True
                elif not request_param_name.endswith('[]'):
                    list_param_name = f'{request_param_name}[]'
                    if list_param_name in method:
                        return method.getlist(list_param_name), True
        if raise_exception:
            raise ValueError(f'No field {request_param_name} in request')
        else:
            return default_value, False
    else:
        if raise_exception:
            raise ValueError('Request parameter name empty')
        else:
            return default_value, False
