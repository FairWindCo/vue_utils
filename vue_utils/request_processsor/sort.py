from typing import Iterable, Union

from django.db.models import QuerySet


# noinspection PyUnusedLocal
def sort_queryset(query_set: QuerySet, sort_multi: Iterable = None, sort_field: str = None,
                  sort_order: Union[str, int, bool] = True, default_sorting: Union[str, Iterable] = None,
                  sort_only_fields: Iterable = None, check_filed_before_sort: bool = False, **kwarg: dict) -> QuerySet:
    """
    sort QuerySet
    Сортировка набора данных с указанными параметрамиб с поддержкой сортировки по одному полю заданному sort_field или
    множеству полей sort_multi (указанных списком вловарей со ключами  field и order
    Порядок сортировки задается значением 1 и -1 (по возрастснию и по убыванию соотвественно)
    :rtype: QuerySet results with  sorting
    :param check_filed_before_sort: flag that indicate test sorted fields name in  sort_only_fields list
    (for sorting only specified fields)
    :param default_sorting:  if no sorting (sort_field or sort_multi) specified use default_sorting
    :param sort_field: field for sorting (no multiply sorting)
    :param sort_multi: complex multi sorting
    (list of dict {
        filed - field name,
        order - "1" asc
                "-1" desc
        }
    )
    :param query_set: QuerySet for apply sorting operation
    :param sort_order: order value 1 asc, value -1  is desc
    :type sort_only_fields: object
    """
    if query_set and (isinstance(query_set, QuerySet) or hasattr(query_set, 'order_by')):
        if sort_field:
            if not check_filed_before_sort or sort_field in sort_only_fields:
                sort_multi = [{'field': sort_field, 'order': sort_order}]
        if sort_multi:
            sorting = [
                f"{sort_info['field']}" if sort_info['order'] == 1 or sort_info[
                    'order'] == '1' else f"-{sort_info['field']}"
                for sort_info in sort_multi
                if not check_filed_before_sort or sort_info['field'] in sort_only_fields
            ]
            query_set = query_set.order_by(*sorting)
        elif default_sorting:
            if isinstance(default_sorting, str):
                query_set = query_set.order_by(default_sorting)
            elif isinstance(default_sorting, Iterable):
                query_set = query_set.order_by(*default_sorting)
    return query_set
