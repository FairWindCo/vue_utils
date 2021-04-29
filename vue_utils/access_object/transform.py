from inspect import ismethod
from typing import Any, Union, List, Tuple, Dict, Iterable, Callable

from vue_utils.access_object.detect_type import is_not_string_sequence, is_dict, is_primitive


def simplify_object(obj: Any) -> Union[dict, list, float, bool, str, int]:
    """
    Function convert difficult object like class to simple dict like dict
    :param obj: Any
    :return: dict|list|simple object
    """
    if obj is None:
        return None

    if is_primitive(obj):
        return obj

    if hasattr(obj, "_ast"):
        return to_dict(getattr(obj, "_ast"))

    if is_not_string_sequence(obj):
        return [to_dict(v) for v in obj]

    if is_dict(obj):
        return {key: to_dict(value)
                for key, value in obj.__dict__.items()
                if not callable(value) and not key.startswith('_')}
    # is not iterable, not primitive and not dict may be class
    if hasattr(obj, '__dict__'):
        return {key: to_dict(value)
                for key, value in obj.__dict__.items()
                if not callable(value) and not key.startswith('_')}
    if hasattr(obj, '__slots__'):
        return {key: to_dict(value)
                for key, value in obj.__slots__.items()
                if not callable(value) and not key.startswith('_')}
    return None


def to_dict(obj: Any, value_key: Union[str, int] = None, class_key: str = None) -> Union[
    dict, list, float, bool, str, int]:
    """
    превращает объект в словарь
    :param obj: объект
    :param value_key:str|int имя ключа словаря куда будет записан объект если он не является сам словарем
    :param class_key: ключ куда записать исходное имя класса объекта
    :return: словарь с объектом (или список/простой объект)
    """
    data = simplify_object(obj)
    is_dict_result = is_dict(data)
    if not is_dict_result and not value_key:
        return data
    if not is_dict_result:
        data = {value_key: data}

    if class_key is not None and hasattr(obj, "__class__"):
        data[class_key] = obj.__class__.__name__

    return data


def get_obj_member(obj: Any, member_name: Union[str, int], default_val: any = None, ignore_hidden=False) -> Any:
    if obj and member_name:
        if is_primitive(obj):
            return default_val
        if is_not_string_sequence(obj) and isinstance(member_name, int):
            return default_val if len(obj) <= abs(member_name) else obj[member_name]
        if isinstance(member_name, str):
            if member_name.startswith('_') and ignore_hidden:
                return default_val
            if is_dict(obj):
                return obj.get(member_name, default_val)
            if hasattr(obj, member_name):
                val = getattr(obj, member_name)
                return val
    return default_val


def get_field_value(obj: Any, field_name: Union[str, int], default_val: any = None, can_call_function=True,
                    ignore_method=False) -> Any:
    val = get_obj_member(obj, field_name, default_val)
    if can_call_function and callable(val):
        if ismethod(val) and not ignore_method:
            val = val()
        else:
            val = val()
    return val


def get_from_container(container, field_list_with_default_values: List[Tuple[str, any]],
                       use_container_as_value: bool = False,
                       ignore_iterable: bool = False):
    if isinstance(container, str) and use_container_as_value:
        result = [def_value for field_name, def_value in field_list_with_default_values]
        result[0] = container
    elif isinstance(container, Dict):
        result = [container.get(field_name, def_value) for field_name, def_value in field_list_with_default_values]
    elif not ignore_iterable and isinstance(container, Iterable):
        result = [def_value for field_name, def_value in field_list_with_default_values]
        for index, value_for_field in enumerate(container[:len(result)]):
            result[index] = value_for_field
    elif use_container_as_value:
        result = [def_value for field_name, def_value in field_list_with_default_values]
        result[0] = container
    else:
        result = None
    return result


def dict_serializer(list_object: Iterable):
    return [to_dict(obj) for obj in list_object]


def standard_value_converter(value: Any, converter: Union[str, callable], ignore_conversion_error: bool = True,
                             default_convert_to_dict: bool = True, custom_serialized: Callable = None) -> object:
    converted_value = None
    if value is not None and converter:
        try:
            if callable(converter):
                converted_value = converter(value)
            elif isinstance(converter, str):
                if converter == 'int':
                    converted_value = int(value)
                elif converter == 'float':
                    converted_value = float(value)
                elif converter == 'bool':
                    converted_value = bool(value)
                elif converter == 'bool_not':
                    converted_value = not bool(value)
                elif converter == 'dict':
                    converted_value = to_dict(value)
                elif converter.startswith('serialize'):
                    field_def = converter[9:-1].split(',')
                    if field_def and custom_serialized:
                        converted_value = custom_serialized(value, field_def)
                    else:
                        converted_value = to_dict(value)
                else:
                    converted_value = str(value)
        except ValueError as err:
            print('Convert value error')
            if not ignore_conversion_error:
                raise err
            else:
                print('Convert value error')
                return None
    elif value is not None:
        if hasattr(value, 'serializer'):
            serializer = getattr(value, "serializer", None)
            if callable(serializer):
                return serializer(value)
            return None
        elif isinstance(value, (int, float, bool, str)) or not default_convert_to_dict:
            converted_value = str(value)
        elif default_convert_to_dict:
            converted_value = to_dict(value)
        else:
            converted_value = str(value)
    else:
        if converter == 'bool':
            return False
        elif converter == 'bool_not':
            return True
    return converted_value
