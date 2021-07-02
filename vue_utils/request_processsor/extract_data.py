from typing import Union, Iterable

from django.db.models import QuerySet

from vue_utils.access_object.transform import get_from_container


# noinspection PyUnusedLocal
def extract_view_queryset(query_set: QuerySet, viewed_fields: Union[str, Iterable] = None, 
                          select_all_field:bool=True, **kwagrs) -> QuerySet:
    """
    Extract only specified field from dataset
    Указывает оставить в результррующем наборе данных только указанные поля
    :param query_set: QuerySet for data extraction
    :type viewed_fields: list of field for data extraction
    :rtype: QuerySet that contains only specified fields
    """
    if not select_all_field and viewed_fields is not None and \
            viewed_fields and query_set and (isinstance(query_set, QuerySet) or hasattr(query_set, 'values')):
        if isinstance(viewed_fields, str):
            viewed_fields = viewed_fields.split(',')
        view_field_desc = [get_from_container(field_name, [('field_name', None)], True)[0] for field_name in
                           viewed_fields]
        query_set = query_set.values(*view_field_desc)
    return query_set
