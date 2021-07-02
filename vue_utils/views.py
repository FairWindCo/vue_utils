from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as lang
# Create your views here.
from django.views.generic import ListView

from vue_utils.request_processsor.filter_creators import compute_filters
from vue_utils.request_processsor.serialize import my_serializer
from vue_utils.request_processsor.view import apply_filter_to_query_set, return_result_context


def view_test(request):
    return render(request, 'vue_utils/vue_base_template.html', context={})


class FilterListView(ListView):
    """A base view for displaying a list of objects."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_transform_configuration = {}
        self.user_defined_paging = self.paginate_by
        self.user_defined_sort = self.ordering
        self.last_request = None
        self.last_combined_filter = None
        self.last_filter_values = None
        
        if self.filters_fields is None and self.model:
            self.filters_fields = [field_def.name for field_def in self.model._meta.fields]
            
        if self.viewed_fields is None and self.model:
            self.viewed_fields = [field_def.name for field_def in self.model._meta.fields]

    # Поля для по для фильтрации с описаниями:
    # Список из:
    # str - название поля
    # dict(    'field_name' - имя поля
    #          'field_action' - действие фильтрации icontains, exact, iexact, contains, in, gt, gte, lt, lte, ....
    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#id4
    #          'form_field_name' - имя поля в форме
    #          'form_field_converter' - преобразователь занчений формы (конвенртор)
    # )
    # tuple(   имя поля,
    #          действие фильтрации icontains, equal, ....,
    #          имя поля в форме,
    #          преобразователь занчений формы (конвенртор)
    # )
    filters_fields = None
    # Метод поиска по умолчанию
    default_filter_action = 'icontains'
    # Дополнительные атрибуты которые передаются в шаблон
    additional_static_attribute = {}
    filter_form_values = {}
    # Поля для отображения (список имен)
    viewed_fields = None

    page_row_request_field = 'per_page'
    sort_request_field = 'sort_by'
    page_request_field = 'page'
    default_ordering = 'id'
    # use filter fields like __contains
    use_extended_filter = False
    # use complex filter field in request
    use_combined_filter = 'view_filter'
    select_all_fields = True

    def get_additional_context_attribute(self):
        return {}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        add_context = self.get_additional_context_attribute()
        if add_context:
            context.update(**add_context)
        if self.additional_static_attribute:
            context.update(**self.additional_static_attribute)

        if self.filter_form_values:
            context.update(**{'filter_form_values': self.filter_form_values})
        return context

    def get_queryset(self):                        
        list_objects = super().get_queryset()

        if self.last_request and self.filters_fields:
            combined_filter = compute_filters(self.last_request, self.filters_fields,
                                              use_combined_filter=self.use_combined_filter,
                                              default_filter_action=self.default_filter_action,
                                              page_row_request_field=self.page_row_request_field,
                                              sort_request_field=self.sort_request_field,
                                              page_request_field=self.page_request_field,
                                              default_ordering=self.default_ordering,
                                              use_extended_filter=self.use_extended_filter,                                              
                                              **self.filter_transform_configuration)
            self.last_combined_filter = combined_filter
            list_objects, self.last_filter_values = apply_filter_to_query_set(list_objects, combined_filter,
                                                                              filters_fields=self.filters_fields,
                                                                              viewed_fields=self.viewed_fields,
                                                                              select_all_field=self.select_all_fields,
                                                                              **self.filter_transform_configuration)
        return list_objects

    def get(self, request, *args, **kwargs):
        self.last_request = request
        return super(FilterListView, self).get(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        # self.last_request = request
        # return super(FilterListView, self).get(request, *args, *kwargs)
        return self.get(request, *args, **kwargs)


class FilterAjaxListView(FilterListView):
    # viewed_fields - Поля для по для отображения:
    # Список из:
    # str - название поля
    # dict(    'field_name' - имя поля
    #          'convertor' - преобразователь занчений формы (конвенртор)
    # )
    # tuple(   имя поля,
    #          преобразователь занчений формы (конвенртор)
    # )
    incorrect_page_as_empty_list = True
    serialized_fields = None
    standard_serializer = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.last_request = request
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.

            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(lang('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        serializer = my_serializer

        if self.standard_serializer:
            serializer = self.standard_serializer
        elif hasattr(self.model, 'serializer'):
            serializer = self.model.serializer

        page_size = self.get_paginate_by(self.object_list)
        page_size = self.last_combined_filter.get('per_page', page_size)
        page = self.last_combined_filter.get('page', 0)

        context = return_result_context(self.object_list,
                                        page=page, paginate_by=page_size,
                                        serialize_config=self.serialized_fields, 
                                        custom_serializer=serializer)

        add_context = self.get_additional_context_attribute()
        if add_context:
            context.update(**add_context)
        if self.additional_static_attribute:
            context.update(**self.additional_static_attribute)

        return JsonResponse(context)
