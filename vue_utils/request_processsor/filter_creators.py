import json
from typing import Dict, Iterable

from django.db.models import Q

from vue_utils.access_object.transform import get_from_container, standard_value_converter
from vue_utils.request_processsor.utility import get_extended_filed, get_from_request


def form_filter_dict(request, filter_list, default_filter_action='icontains'):
    if filter_list:
        filter_dict = {}
        form_values = {}
        form_field_converter = None
        value_as_filter = True
        for filter_field_name in filter_list:
            current_field = None
            form_field_name = None
            filter_action = None
            filter_null = True
            if isinstance(filter_field_name, str):
                current_field = filter_field_name
                filter_action = default_filter_action

            elif isinstance(filter_field_name, Dict) or isinstance(filter_field_name, Iterable):
                current_field, filter_action, form_field_name, form_field_converter, \
                value_as_filter, filter_null = get_from_container(
                    filter_field_name, [
                        ('field_name', None),
                        ('field_action', default_filter_action),
                        ('form_field_name', None),
                        ('form_field_converter', None),
                        ('value_as_filter', True),
                        ('filter_null', True),
                    ])
            if form_field_name is None:
                form_field_name = current_field

            value, exist_in_request = get_from_request(request, form_field_name)
            if current_field and value:
                if not isinstance(value, str) and (isinstance(value, Dict) or isinstance(value, Iterable)):
                    current_value, filter_action = get_from_container(value, [
                        ('value', None),
                        ('action', filter_action)
                    ], True, ignore_iterable=not value_as_filter)
                else:
                    current_value = value
                current_value = standard_value_converter(current_value, form_field_converter)
                if current_value:
                    if filter_action:
                        filter_dict[f'{current_field}__{filter_action}'] = current_value
                    else:
                        filter_dict[f'{current_field}'] = current_value
                    form_values[form_field_name] = current_value
            elif filter_null and current_field and exist_in_request:
                filter_dict[f'{current_field}__isnull'] = True

        return filter_dict, form_values
    else:
        return None, None


# noinspection PyUnusedLocal
def form_filters_from_request(request, filter_list,
                              default_filter_action='icontains',
                              use_extended_filter=False,
                              page_row_request_field='per_page',
                              sort_request_field='sort_by',
                              page_request_field='page',
                              default_ordering='id',
                              **kwagrs):
    paginate_by, _ = get_from_request(request, page_row_request_field, None)
    ordering, _ = get_from_request(request, sort_request_field, default_ordering)
    page_number, _ = get_from_request(request, page_request_field, 0)

    process = {
        'page': page_number,
        'per_page': paginate_by,
        'sort_field': ordering,
        'filters': {

        },
        'filter_field_name_list':[],
    }

    if filter_list:
        for filter_field_name in filter_list:
            if isinstance(filter_field_name, str):
                current_field = filter_field_name
                form_field_name = current_field
                filter_action = default_filter_action
                value_as_filter = True
                filter_null = None
                form_field_converter = None

            elif isinstance(filter_field_name, Dict) or isinstance(filter_field_name, Iterable):
                current_field, filter_action, form_field_name, form_field_converter, \
                value_as_filter, filter_null = get_from_container(
                    filter_field_name, [
                        ('field_name', filter_field_name),
                        ('field_action', default_filter_action),
                        ('form_field_name', None),
                        ('form_field_converter', None),
                        ('value_as_filter', True),
                        ('filter_null', True),
                    ])
                form_field_name = form_field_name if form_field_name else current_field
            else:
                continue
            if use_extended_filter:
                value, exist_in_request, current_field = get_extended_filed(request, form_field_name)
            else:
                value, exist_in_request = get_from_request(request, form_field_name)
            if current_field and exist_in_request:

                if not isinstance(value, str) and (isinstance(value, Dict) or isinstance(value, Iterable)):
                    current_value, filter_action = get_from_container(value, [
                        ('value', None),
                        ('action', filter_action)
                    ], True, ignore_iterable=not value_as_filter)
                else:
                    current_value = value
                current_value = standard_value_converter(current_value, form_field_converter)
                process['filter_field_name_list'].append(current_field)
                process['filters'][current_field] = {
                    'value': current_value,
                    'form_field': form_field_name,
                    'matchMode': filter_action,
                    'filter_null': filter_null
                }
    return process


def translate_operators(operator: str, operator_conversion: Dict[str, str] = None) -> (str, bool):
    if operator_conversion is None:
        operator_conversion = {
            'startsWith': ('istartswith', False),
            'endWith': ('iendwith', False),
            'Contains': ('contains', False),
            'notContains': ('contains', True),
            'Equal': ('equal', False),
            'notEqual': ('equal', True),
            '==': ('', False),
            '!=': ('', True),
        }
    return operator_conversion.get(operator, (operator, False))


def update_filter_def(field_name, filter_def=None, field_value=None, field_operation=None, reverse=False,
                      filter_null=True,
                      current_query_index=None, or_operation=False, special_name=False):
    if filter_def is None:
        filter_def = []
    index = None
    if field_name:
        if field_value is None and not filter_null and not field_name.endswith('__isnull'):
            return filter_def, index
        if (filter_null and not field_value) or field_name.endswith('__isnull'):
            q = {f'{field_name}__isnull': True}
        elif field_operation and not special_name:
            q = {f'{field_name}__{field_operation}': field_value}
        else:
            q = {f'{field_name}': field_value}
        query = Q(**q)
        if reverse:
            query = ~query
        if current_query_index:
            current_query = filter_def[current_query_index]
            query = current_query.OR(query) if or_operation else current_query.AND(query)
            filter_def[current_query_index] = query
        else:
            index = len(filter_def)
            filter_def.append(query)
    return filter_def, index


def preprocess_combined_filter(filter_def):
    if filter_def and isinstance(filter_def, Dict):
        for name, new_name in {'sortField': 'sort_field',
                               'multiSortMeta': 'sort_multi',
                               'sortOrder': 'sort_order'}.items():
            if name and new_name and name in filter_def:
                filter_def[new_name] = filter_def[name]
    return filter_def


# noinspection PyUnusedLocal
def compute_filters(request, filters_fields,
                    use_combined_filter='view_filter', default_filter_action='icontains',
                    page_row_request_field='per_page',
                    sort_request_field='sort_by',
                    page_request_field='page',
                    default_ordering='id',
                    use_extended_filter=False,
                    print_filter_info=False, **kwargs):
    combined_filter = None
    if request and filters_fields:
        combined_filter, in_request = get_from_request(request, use_combined_filter, None)
        if in_request:
            if isinstance(combined_filter, str):
                try:
                    combined_filter = preprocess_combined_filter(json.loads(combined_filter))
                except Exception:
                    combined_filter = None
        else:
            combined_filter = form_filters_from_request(request, filters_fields,
                                                        default_filter_action=default_filter_action,
                                                        use_extended_filter=use_extended_filter,
                                                        page_row_request_field=page_row_request_field,
                                                        sort_request_field=sort_request_field,
                                                        page_request_field=page_request_field,
                                                        default_ordering=default_ordering,
                                                        **kwargs)
    if print_filter_info:
        print(combined_filter)
    return combined_filter
