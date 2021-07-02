from typing import Iterable

from django.db.models import QuerySet

from vue_utils.request_processsor.filter_creators import translate_operators, update_filter_def
from vue_utils.request_processsor.utility import special_name_part


# noinspection PyUnusedLocal
def filter_queryset(query_set: QuerySet, filters: dict,
                    filters_fields: Iterable = None,
                    default_filter_action: str = None,
                    default_operator_conversion: object = None,
                    filter_null: bool = False,
                    check_special_names: bool = True,
                    check_filed_before_filter: bool = True,
                    **kwarg: dict) -> (QuerySet, dict):
    filter_values = {}
    if filters is not None and filters and query_set and (isinstance(query_set, QuerySet) or \
            hasattr(query_set, 'filter')):
        where_filter = []
        for field_for_filtering in filters:
            if check_special_names:
                is_special_name, original_name = special_name_part(field_for_filtering)
            else:
                is_special_name, original_name = False, ''
                # check that field specified in filters_fields (if not skip this field)
            if check_filed_before_filter and (field_for_filtering not in filters_fields and
                                              (is_special_name and original_name not in filters_fields)):
                continue

            filter_def = filters[field_for_filtering]
            if isinstance(filter_def, dict):
                constrains = filter_def.get('constraints', [])
                if constrains:
                    current_query = None
                    or_operator = True if filter_def.get('operator', 'AND') == 'or' else False
                    for constraint in constrains:
                        value = constraint.get('value', None)
                        form_field = constraint.get('form_field', field_for_filtering)
                        current_null_filter = constraint.get('filter_null', filter_null)
                        operation, invert = translate_operators(constraint.get('matchMode', None),
                                                                default_operator_conversion)
                        where_filter, current_query = update_filter_def(field_for_filtering,
                                                                        where_filter,
                                                                        value,
                                                                        operation, invert,
                                                                        current_null_filter, current_query,
                                                                        or_operator, is_special_name)
                        filter_values[form_field] = value
                else:
                    value = filter_def.get('value', None)
                    form_field = filter_def.get('form_field', field_for_filtering)
                    operation, invert = translate_operators(filter_def.get('matchMode', None),
                                                            default_operator_conversion)
                    current_null_filter = filter_def.get('filter_null', filter_null)
                    _, _ = update_filter_def(field_for_filtering, where_filter, value,
                                             operation, invert,
                                             current_null_filter, special_name=is_special_name)
                    filter_values[form_field] = value
            else:
                _, _ = update_filter_def(field_for_filtering, where_filter, filter_def,
                                         *translate_operators(default_filter_action,
                                                              default_operator_conversion),
                                         filter_null, special_name=is_special_name)
                filter_values[field_for_filtering] = filter_def
        if where_filter:
            query_set = query_set.filter(*where_filter)

    return query_set, filter_values
