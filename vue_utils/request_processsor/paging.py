from typing import Sized

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import Http404


# noinspection PyUnusedLocal
def paging_queryset(query_set: QuerySet, page: int = 0, per_page: int = None, is_for_ajax: bool = False,
                    **kwarg: dict) -> (QuerySet, dict):
    page_info = {
        'page': 1,
        'per_page': per_page,
        'pages': 1,
        'count': 0,
        'count_e': 0,
        'paginator': None,
        'page_object': None,
        'page_list': query_set if not is_for_ajax else (),
        'is_paginated': False
    }
    if query_set or isinstance(query_set, QuerySet):
        if page > 0 and per_page:
            if isinstance(query_set, QuerySet) or hasattr(query_set, 'count'):
                paginate_by = int(per_page) if isinstance(per_page, (int, float)) else 10
                page = int(page) if isinstance(page, (int, float)) else 1
                try:
                    paginator = Paginator(query_set, paginate_by)
                    page_info['count_e'] = paginator.count
                    page_info['count'] = query_set.count()
                    page_info['page'] = page
                    page_info['pages'] = paginator.num_pages
                    page_info['per_page'] = paginate_by
                    query_set = paginator.get_page(page)
                    page_info['page_object'] = query_set
                    page_info['page_list'] = query_set.object_list
                    if not is_for_ajax:
                        page_info['paginator'] = paginator
                    page_info['is_paginated'] = True
                except Http404:
                    query_set = ()
                    page_info['count_e'] = 0
                    page_info['count'] = 0
                    page_info['page'] = page
                    page_info['pages'] = 1
                    page_info['per_page'] = paginate_by
        else:
            if isinstance(query_set, QuerySet) or hasattr(query_set, 'count'):
                page_info['count'] = query_set.count()
            elif hasattr(query_set, '__len__') or isinstance(query_set, Sized):
                page_info['count'] = len(query_set)
            else:
                page_info['count'] = 1
            page_info['page_list'] = query_set
    return query_set, page_info
