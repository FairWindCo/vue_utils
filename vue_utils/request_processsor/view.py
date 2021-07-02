from typing import Any, Union, Iterable

from django.db.models import QuerySet
from vue_utils.access_object.transform import dict_serializer
from vue_utils.request_processsor.extract_data import extract_view_queryset
from vue_utils.request_processsor.filter import filter_queryset
from vue_utils.request_processsor.filter_creators import compute_filters
from vue_utils.request_processsor.paging import paging_queryset
from vue_utils.request_processsor.serialize import serialize_queryset, my_serializer
from vue_utils.request_processsor.sort import sort_queryset
from vue_utils.request_processsor.utility import get_from_request


def operate_query_set(query_set: QuerySet,
                      filters: dict,
                      filters_fields: Iterable = None,
                      default_filter_action: str = None,
                      default_operator_conversion: object = None,
                      filter_null: bool = False,
                      check_special_names: bool = True,
                      check_filed_before_filter: bool = True,
                      sort_multi: Iterable = None,
                      sort_field: str = None,
                      sort_order: Union[str, int, bool] = True,
                      default_sorting: Union[str, Iterable] = None,
                      sort_only_fields: Iterable = None,
                      check_filed_before_sort: bool = False,
                      viewed_fields: Union[str, Iterable] = None,
                      select_all_field: bool = True,
                      **kwargs) -> (QuerySet, dict):
    query_set, filter_values = filter_queryset(query_set, filters=filters,
                                               filters_fields=filters_fields,
                                               default_filter_action=default_filter_action,
                                               default_operator_conversion=default_operator_conversion,
                                               filter_null=filter_null,
                                               check_special_names=check_special_names,
                                               check_filed_before_filter=check_filed_before_filter,
                                               **kwargs)

    query_set = sort_queryset(query_set, sort_multi=sort_multi, sort_field=sort_field,
                              sort_order=sort_order, default_sorting=default_sorting,
                              sort_only_fields=sort_only_fields,
                              check_filed_before_sort=check_filed_before_sort,
                              **kwargs)

    query_set = extract_view_queryset(query_set, viewed_fields=viewed_fields,
                                      select_all_field=select_all_field, **kwargs)

    return query_set, filter_values


def apply_filter_to_query_set(query_set: QuerySet, combined_filter: dict,
                              filters_fields: Iterable = None,
                              default_filter_action: str = None,
                              default_operator_conversion: object = None,
                              filter_null: bool = False,
                              check_special_names: bool = True,
                              check_filed_before_filter: bool = True,
                              default_sorting: Union[str, Iterable] = None,
                              sort_only_fields: Iterable = None,
                              check_filed_before_sort: bool = False,
                              viewed_fields: Union[str, Iterable] = None,
                              select_all_field: bool = True,
                              **kwargs) -> (QuerySet, dict):
    filters = combined_filter.get('filters', [])
    sort_multi = combined_filter.get('sort_multi', [])
    sort_field = combined_filter.get('sort_field', None)
    sort_order = combined_filter.get('sort_order', '1')

    return operate_query_set(query_set,
                             filters=filters,
                             filters_fields=filters_fields,
                             default_filter_action=default_filter_action,
                             default_operator_conversion=default_operator_conversion,
                             filter_null=filter_null,
                             check_special_names=check_special_names,
                             check_filed_before_filter=check_filed_before_filter,
                             sort_multi=sort_multi, sort_field=sort_field,
                             sort_order=sort_order, default_sorting=default_sorting,
                             sort_only_fields=sort_only_fields,
                             check_filed_before_sort=check_filed_before_sort,
                             viewed_fields=viewed_fields, select_all_field=select_all_field,
                             **kwargs)


def return_result_context(list_objects, page: int = None, paginate_by: int = None,
                          serialize_config: dict = None, custom_serializer=dict_serializer):
    list_objects, page_info = paging_queryset(list_objects, page, paginate_by)
    return serialize_queryset(list_objects, page_info, custom_serializer=custom_serializer,
                              serialize_config=serialize_config, form_complex_response=True)


def process_paging(request, objects: Any, default_page_size: int = '25', serializer=dict_serializer):
    page_number, _ = get_from_request(request, 'page', 0)
    page_size, _ = get_from_request(request, 'per_page', default_page_size)
    return return_result_context(objects, page_number, page_size, custom_serializer=serializer)


def user_controlled_view(list_objects, view_dict,
                         filters_fields=None,
                         default_attribute=None,
                         viewed_fields=None):
    if default_attribute is None:
        default_attribute = {
            'per_page': 10,
        }
    serializer_config = default_attribute.get('serializer_config', None)
    serializer = default_attribute.get('serializer', my_serializer)
    if view_dict:
        default_attribute.update(view_dict)
    page = default_attribute.get('page', 1)
    per_page = default_attribute.get('per_page', 10)
    list_objects, _ = operate_query_set(list_objects,
                                        filters_fields=filters_fields,
                                        viewed_fields=viewed_fields,
                                        **default_attribute)
    return return_result_context(list_objects, page, per_page, serializer_config, serializer)


def filter_query(request, list_objects, filters_fields, viewed_fields=None, configuration=None):
    if configuration is None:
        configuration = {}
    combined_filter = compute_filters(request, filters_fields, **configuration)

    return user_controlled_view(list_objects, combined_filter, filters_fields, configuration, viewed_fields)

# def controlled_filter(list_objects, view_dict, filters_fields=None, default_attribute=None, viewed_fields=None):
#     if default_attribute is None:
#         default_attribute = {}
#     if view_dict:
#         default_attribute.update(view_dict)
#     if viewed_fields:
#         default_attribute.update(viewed_fields)
#     default_attribute['filters_fields'] = filters_fields
#     list_objects, filter_values = filter_queryset(list_objects, **default_attribute)
#     list_objects = sort_queryset(list_objects, **default_attribute)
#     list_objects = extract_view_queryset(list_objects, **default_attribute)
#     return list_objects, filter_values
