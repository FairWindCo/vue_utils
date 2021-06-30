import glob
import glob
import os
from typing import Iterable, Dict, Any

from PIL import Image
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Manager, QuerySet
# Метод возвращает значение поля из запроса
from django.http import Http404

from vue_utils.access_object.detect_type import is_dict, is_not_string_sequence
from vue_utils.access_object.transform import to_dict, standard_value_converter, get_from_container, dict_serializer


def get_from_request(request, request_param_name: str, default_value: Any = None, raise_exception: bool = False,
                     request_methods: Iterable[str] = ('GET', 'POST')) -> (Any, bool):
    if request is None:
        if raise_exception:
            raise ValueError('Request is None')
        else:
            return default_value, False
    if request_param_name:
        for method_name in request_methods:
            method = get_field_value(request, method_name, None)
            if method:
                if request_param_name in method:
                    return method.get(request_param_name), True
                elif not request_param_name.endswith('[]'):
                    list_param_name = f'{request_param_name}[]'
                    if list_param_name in method:
                        return method.getlist(list_param_name), True
            if raise_exception:
                raise ValueError(f'No field {request_param_name} in request')
            else:
                return default_value, False
    else:
        if raise_exception:
            raise ValueError('Request parameter name empty')
        else:
            return default_value, False


def standard_serializer(list_object: Any):
    return serializers.serialize('json', list_object)


def get_field_value(obj: any, field_name: str, default_val: any = None, can_call_function=True):
    if obj and field_name:
        if is_dict(obj):
            return obj.get(field_name, default_val)
        elif is_not_string_sequence(obj) and field_name.isnumeric():
            index = int(field_name)
            return default_val if len(obj) <= index else obj[index]
        elif hasattr(obj, field_name):
            val = getattr(obj, field_name)
            if can_call_function and callable(val) and not isinstance(val, Manager):
                val = val()
            return val
        else:
            return default_val
    else:
        return default_val


def get_field_value_ex(obj: any, field_name: str, default_val: any = None, can_call_function=True):
    if obj is None:
        return default_val
    if '__' in field_name:
        fields = field_name.split('__')
        if fields:
            val = obj
            for field in fields:
                val = get_field_value(val, field, default_val)
                if val is None:
                    break
            return val
        return default_val
    else:
        return get_field_value(obj, field_name, default_val)


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


def process_paging(request, objects: Any, default_page_size: int = '25', serializer=dict_serializer):
    page_number, _ = get_from_request(request, 'page', 0)
    page_size, _ = get_from_request(request, 'per_page', default_page_size)
    paginator = Paginator(objects, page_size)

    return {
        'list': serializer(paginator.get_page(page_number).object_list),
        'page_number': page_number,
        'per_page': page_size,
        'count': paginator.count
    }


# Метод производит генерацию словаря для фильтрации из данных формы полученной GET или POST запросом
#  request - объект Request из запроса
# filter_list - описание полей в форме сиска содержащего строки с именами полей или словарь с полями
# dict(    'field_name' - имя поля
#          'field_action' - действие фильтрации icontains, equal, .... (не обязательное)
#          'form_field_name' - имя поля в форме (не обязательное)
#          'form_field_converter' - преобразователь занчений формы (конвенртор) (не обязательное)
#          'filter_as_value' - указывать разбирать значение формы как пару значение формы и действие
# )
# или tuple со значениями
# tuple(   имя поля,
#          действие фильтрации icontains, equal, ...., (не обязательное)
#          имя поля в форме, (не обязательное)
#          преобразователь занчений формы (конвенртор) (не обязательное)
# )
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


def create_thumbnail(original_file, thb_file_name, size=(100, 60)):
    image = Image.open(original_file)
    image.thumbnail(size)
    image.save(thb_file_name)


def get_image_data(catalog, template, title='Car Photo ', thb_size=(150, 90), prepend_url=''):
    result = []
    filter_ref = catalog + '/' + template
    if os.path.exists(catalog) and os.path.isdir(catalog):
        count = 0
        for infile in glob.glob(filter_ref):
            count += 1
            base_name = os.path.basename(infile)
            path = os.path.dirname(infile)
            thd_name = 'thb_' + base_name
            thd_file = os.path.join(path, thd_name)
            if not os.path.exists(thd_file):
                create_thumbnail(infile, thd_file, thb_size)

            result.append({
                'itemImageSrc': f'{prepend_url}/{base_name}' if prepend_url else base_name,
                'thumbnailImageSrc': f'{prepend_url}/{thd_name}' if prepend_url else thd_name,
                'title': f'{title} {count}'
            })
    return result


def filter_query(request, list_objects, filters_fields, default_filter_action=None, viewed_fields=None,
                 serialize_config=None):
    paginate_by = None
    if hasattr(list_objects, 'filter'):
        if request and filters_fields:
            filter_def, filter_form_values = form_filter_dict(request, filters_fields,
                                                              default_filter_action)
            paginate_by, _ = get_from_request(request, 'per_page', None)
            ordering, _ = get_from_request(request, 'sort_by', 'id')

            if filter_def:
                # print(filter_def, self.filter_form_values)
                list_objects = list_objects.filter(**filter_def)
            if ordering:
                if isinstance(ordering, Iterable) and not isinstance(ordering, str):
                    list_objects = list_objects.order_by(*ordering)
                else:
                    list_objects = list_objects.order_by(ordering)
        if viewed_fields:
            view_field_desc = [get_from_container(field_name, [('field_name', None)], True)[0] for field_name in
                               viewed_fields]
            list_objects = list_objects.values(*view_field_desc)
    context = {}
    if paginate_by:
        try:
            page_number, _ = get_from_request(request, 'page', 0)
            paginator = Paginator(list_objects, paginate_by)
            count = list_objects.count()
            page = paginator.get_page(page_number)
            context['data_count'] = count
            context['data_list'] = page.object_list
            context['page_count'] = paginator.num_pages
            context['page'] = page.number
        except Http404:
            context['data_list'] = []
            count = list_objects.count
            context['data_count'] = count
            context['page_count'] = count % int(paginate_by) + 1
            context['page'], _ = get_from_request(request, 'page', 0)
    else:
        context['data_list'] = list_objects
        context['data_count'] = len(list_objects)
    context['data_list'] = my_serializer(context['data_list'], serialize_config)
    return context
