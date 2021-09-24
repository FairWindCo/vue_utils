import django
from django.forms import CharField, HiddenInput, Field
from django.http import Http404, JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.translation import gettext as lang
# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin, DeletionMixin, ProcessFormView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, DetailView, BaseDetailView
from django.views.generic.base import ContextMixin
from vue_utils.request_processsor.filter_creators import compute_filters
from vue_utils.request_processsor.paging import paging_queryset
from vue_utils.request_processsor.serialize import my_serializer, serialize_queryset
from vue_utils.request_processsor.utility import get_from_request
from vue_utils.request_processsor.view import exec_filter_sort_view_queryset


def view_test(request):
    return render(request, 'vue_utils/vue_base_template.html', context={})


class FilterListView(ListView):
    """A base view for displaying a list of objects."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_transform_configuration = {}
        self.user_defined_paging = self.paginate_by
        self.user_defined_sort = self.ordering
        # Последний запрос
        self.last_request = None
        # Последний сформированный фильтр полученный при разборе запроса
        self.last_combined_filter = None
        self.last_page_info = None
        # Значение фильтров полученный при разборе запроса
        self.filter_form_values = {}

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
    # Поля для отображения (список имен)
    viewed_fields = None

    default_filter_action = 'icontains'
    # Дополнительные атрибуты которые передаются в шаблон
    additional_static_attribute = {}

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
        context = super(FilterListView, self).get_context_data(object_list=object_list, **kwargs)
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
            list_objects, self.filter_form_values = exec_filter_sort_view_queryset(list_objects, combined_filter,
                                                                                   filters_fields=self.filters_fields,
                                                                                   viewed_fields=self.viewed_fields,
                                                                                   select_all_field=self.select_all_fields,
                                                                                   **self.filter_transform_configuration)
            page_size = self.get_paginate_by(list_objects)
            page_size = int(self.last_combined_filter.get('per_page', page_size))
            page = int(self.last_combined_filter.get('page', 0))
            list_objects, self.last_page_info = paging_queryset(list_objects, page, page_size)

        return list_objects

    def get_paginate_by(self, queryset):
        if self.last_page_info:
            return self.last_page_info['per_page']
        return super(FilterListView, self).get_paginate_by(queryset)

    def paginate_queryset(self, queryset, page_size):
        if self.last_page_info and self.last_page_info['is_paginated']:
            return  self.last_page_info['paginator'], \
                    self.last_page_info['page_object'], \
                    self.last_page_info['page_list'], \
                    self.last_page_info['is_paginated']
        return super(FilterListView, self).paginate_queryset(queryset, page_size)

    def get(self, request, *args, **kwargs):
        self.last_request = request
        return ListView.get(self, request, *args, *kwargs)
        # return super(FilterListView, self).get(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        # self.last_request = request
        return self.get(request, *args, **kwargs)


class CrudView(CreateView, UpdateView, DeleteView, DetailView):
    operation_mark_field = 'operation'
    form_template_name_suffix = '_form'
    delete_template_name_suffix = '_form'
    detail_template_name_suffix = '_detail'
    use_self_success_url = True

    def __init__(self, *args, **kwargs):
        self.operation = None
        self.object = None
        self.csrf_token_for_form = None
        self.request_path = None
        super().__init__(*args, **kwargs)

    def view_object(self, *args, **kwargs):
        context = self.get_context_data()
        print(context)
        return self.render_to_response(context)

    def create_operation(self, request, *arg, **kwarg):
        return ProcessFormView.post(self, request, *arg, **kwarg)

    def update_operation(self, request, *arg, **kwarg):
        self.object = self.get_object()
        return ProcessFormView.post(self, request, *arg, **kwarg)

    def delete_operation(self, request, *arg, **kwarg):
        return DeletionMixin.delete(self, request, *arg, **kwarg)

    def view_for_create(self, request, *arg, **kwarg):
        return self.view_object()

    def view_for_update(self, request, *arg, **kwarg):
        return self.view_object()
        # return BaseDetailView.get(self, request, *arg, **kwarg)

    def view_for_delete(self, request, *arg, **kwarg):
        return self.view_object()

    def view_for_detail(self, request, *arg, **kwarg):
        return self.view_object()

    def get_success_url(self):
        if self.use_self_success_url and self.request_path is not None:
            return self.request_path
        else:
            return super().success_url()


    def get_object(self, queryset=None):
        obj = None
        if self.operation is not None and self.operation != 'create':
            obj = super().get_object(queryset)
            self.object = obj
        return obj

    def get_context_data(self, **kwargs):
        if 'object' not in kwargs:
            obj = self.get_object()
            if obj:
                context_object_name = self.get_context_object_name(obj)
                if context_object_name:
                    kwargs[context_object_name] = obj
                else:
                    kwargs['object'] = obj
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return ContextMixin.get_context_data(self, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields[self.operation_mark_field] = Field(initial=self.operation, widget=HiddenInput)
        if self.csrf_token_for_form is not None:
            form.fields['csrfmiddlewaretoken'] = Field(initial=self.csrf_token_for_form, widget=HiddenInput)
        return form

    def check_operation(self, request, default_template_suffics=''):
        operation, in_request = get_from_request(request, self.operation_mark_field, None)
        self.operation = operation
        self.request_path = request.path
        if in_request:
            if hasattr(django, 'middleware') and hasattr(django.middleware, 'csrf'):
                self.csrf_token_for_form = django.middleware.csrf.get_token(request)
            pk, pk_in_request = get_from_request(request, self.pk_url_kwarg, None)
            slug, slug_in_request = get_from_request(request, self.slug_url_kwarg, None)
            if pk_in_request:
                self.kwargs[self.pk_url_kwarg]=pk
            if slug_in_request:
                self.kwargs[self.slug_url_kwarg]=slug
            if operation == 'create':
                self.template_name_suffix = self.form_template_name_suffix
            elif operation == 'update':
                self.template_name_suffix = self.form_template_name_suffix
            elif operation == 'delete':
                self.template_name_suffix = self.delete_template_name_suffix
            else:
                self.template_name_suffix = self.detail_template_name_suffix
        else:
            self.template_name_suffix = default_template_suffics
        return operation

    def process_get_request(self, request, *args, **kwargs):
        if self.operation == 'create':
            return self.view_for_create(request, *args, **kwargs)
        elif self.operation == 'update':
            return self.view_for_update(request, *args, **kwargs)
        elif self.operation == 'delete':
            return self.view_for_delete(request, *args, **kwargs)
        elif self.operation == 'detail':
            return self.view_for_detail(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()

    def process_post_request(self, request, *args, **kwargs):
        if self.operation == 'create':
            return self.create_operation(request, *args, **kwargs)
        elif self.operation == 'update':
            return self.update_operation(request, *args, **kwargs)
        elif self.operation == 'delete':
            return self.delete_operation(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()

    def get(self, request, *args, **kwargs):
        self.check_operation(request)
        return self.process_get_request(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_operation(request)
        return self.process_post_request(request, *args, **kwargs)


class CrudListView(FilterListView, CrudView):
    operation_mark_field = 'operation'
    list_template_name_suffix = '_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.operation is not None:
            return CrudView.get_context_data(self, **kwargs)
        else:
            self.template_name_suffix = self.list_template_name_suffix
            return FilterListView.get_context_data(self, object_list=object_list, **kwargs)
        
    def get_template_names(self):
        if self.operation is not None:
            return SingleObjectTemplateResponseMixin.get_template_names(self)
        else:
            return FilterListView.get_template_names(self)

    def get(self, request, *args, **kwargs):
        self.check_operation(request)
        if self.operation is None:
            return FilterListView.get(self, request, *args, **kwargs)
        else:
            return CrudView.process_get_request(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_operation(request)
        if self.operation is None:
            return FilterListView.post(self, request, *args, **kwargs)
        else:
            return CrudView.process_post_request(self,request, *args, **kwargs)


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

        context = serialize_queryset(self.object_list, self.last_page_info, custom_serializer=serializer,
                                     serialize_config=self.serialized_fields, form_complex_response=True)

        add_context = self.get_additional_context_attribute()
        if add_context:
            context.update(**add_context)
        if self.additional_static_attribute:
            context.update(**self.additional_static_attribute)

        return JsonResponse(context)
