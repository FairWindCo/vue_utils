from typing import Iterable

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.response import TemplateResponse


def search(request, db_model_class, request_param_name, db_field_name, params_dic):
    if request_param_name in request.POST and request.POST[request_param_name]:
        params_dic[request_param_name] = request.POST[request_param_name]
        return db_model_class.filter(**{db_field_name: request.POST[request_param_name]})
    elif request_param_name in request.GET and request.GET[request_param_name]:
        params_dic[request_param_name] = request.GET[request_param_name]
        return db_model_class.filter(**{db_field_name: request.GET[request_param_name]})
    else:
        return db_model_class


def paginate(request, objects):
    page = request.GET.get('page', 1)
    per_page = request.POST.get('per_page', None)
    if not per_page:
        per_page = request.GET.get('per_page', '10')

    if per_page.isdigit():
        per_page = int(per_page)
    else:
        per_page = 10
    paginator = Paginator(objects, per_page)
    try:
        pager = paginator.page(page)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)
    return pager, pager.number, pager.paginator.per_page


def complex_search(request, db_model_class, **search_params):
    params_dic = {}
    for request_field_name, db_field_name in search_params.items():
        db_model_class = search(request, db_model_class, request_field_name, db_field_name, params_dic)
    return db_model_class, params_dic


def form_context(request, db_model_class, **kwargs):
    if 'result_field_name' in kwargs:
        result_field_name = kwargs['result_field_name']
        del kwargs['result_field_name']
    else:
        result_field_name = 'db_objects'

    if 'search_attributes' in kwargs:
        search_attributes = kwargs['search_attributes']
        del kwargs['search_attributes']
    else:
        search_attributes = {}

    if 'additional_fields' in kwargs:
        additional_fields = kwargs['additional_fields']
        del kwargs['additional_fields']
    else:
        additional_fields = {}

    context_data = kwargs
    search_object, params_dic = complex_search(request, db_model_class, **search_attributes)
    objects, page, per_page = paginate(request, search_object)
    context_data[result_field_name] = objects.object_list
    context_data['page'] = objects
    context_data['page_count'] = per_page
    if additional_fields:
        params_dic.update(additional_fields)
        context_data.update(additional_fields)
    context_data['params'] = params_dic
    return context_data


def request_paginator_form(request, template_name, db_model_class, **kwargs):
    context_data = form_context(request, db_model_class, **kwargs)
    return TemplateResponse(request, template_name, context=context_data)


def get_attribute_from_context(context, attribute_path, need_clean=True):
    d = {}
    if context:
        attributes = attribute_path.split('.')
        for attr in attributes:
            if context:
                if hasattr(context, attr):
                    d = getattr(context, attr, {})
                elif attr in context:
                    d = context[attr]
                else:
                    d = None
                    break
                context = d
            else:
                d = {}
                break
    if need_clean:
        d = create_clean_copy(d)
    return d


def create_clean_copy(iterable_element):
    if type(iterable_element) == str:
        d = iterable_element
    elif isinstance(iterable_element, dict):
        d = {k: v for k, v in iterable_element.items()}
    elif isinstance(iterable_element, set):
        d = {k for k in iterable_element}
    elif isinstance(iterable_element, Iterable):
        d = [k for k in iterable_element]
    else:
        d = iterable_element

    return d
