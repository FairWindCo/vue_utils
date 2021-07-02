from typing import Any, Iterable, Union

from django.core import serializers
from django.db.models import QuerySet

from vue_utils.access_object.transform import get_from_container, standard_value_converter, to_dict, dict_serializer
from vue_utils.request_processsor.utility import get_field_value_ex


def standard_serializer(list_object: Any):
    return serializers.serialize('json', list_object)


def my_list_serializer(serialized_obj_list, serialized_fields, exec_method: bool = True, skip_none: bool = False):
    return [my_serializer(data_object, serialized_fields, exec_method, skip_none)
            for data_object in
            serialized_obj_list]


def my_serializer(serialized_obj, serialized_fields, exec_method: bool = True,
                  skip_none: bool = False):
    result = {}
    if serialized_obj and isinstance(serialized_obj, QuerySet):
        serialized_obj = list(serialized_obj)
    if serialized_fields and (isinstance(serialized_obj, dict) or hasattr(serialized_obj, "__dict__")):
        for field_desc in serialized_fields:
            field_name, convertor, result_field, default_dict, ignore_error = get_from_container(field_desc, [
                ('field_name', None),
                ('convertor', None),
                ('result_field', None),
                ('default_dict', False),
                ('ignore_error', True),
            ], True)

            if result_field is None:
                result_field = field_name

            current_val = get_field_value_ex(serialized_obj, field_name, None, exec_method)

            if current_val:
                result[result_field] = standard_value_converter(current_val, convertor, ignore_error, default_dict,
                                                                my_serializer)
            else:
                if not skip_none:
                    if convertor == 'bool':
                        result[result_field] = False
                    elif convertor == 'bool_not':
                        result[result_field] = True
                    elif convertor == 'str':
                        result[result_field] = ''
                    else:
                        result[result_field] = None
    else:
        result = to_dict(serialized_obj)
    return result


# noinspection PyUnusedLocal
def serialize_queryset(query_set: Union[QuerySet, Iterable],
                       page_info: dict = None,
                       form_complex_response: bool = True,
                       filters_values: dict = None,
                       serialize_config: dict = None,
                       custom_query_set_serializer=None,
                       serialize_query_set: bool = True,
                       custom_serializer=dict_serializer, **kwargs) -> any:
    if serialize_query_set:
        if custom_query_set_serializer and callable(custom_query_set_serializer):
            response = custom_query_set_serializer(query_set, custom_serializer, serialize_config)
        elif custom_serializer and callable(custom_serializer):
            if isinstance(query_set, Iterable) or isinstance(query_set, QuerySet):
                response = [custom_serializer(el, serialize_config) for el in query_set]
            else:
                response = custom_serializer(query_set, serialize_config)
        else:
            response = query_set
    else:
        response = query_set
    if form_complex_response:
        if page_info:
            page_info['list'] = response
            response = page_info
        else:
            response = {'list': response}
        if filters_values:
            response['filters_values'] = filters_values
    return response
