import decimal
from datetime import timedelta

import num2words as num2words
from django import template
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.timesince import timesince

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)


@register.simple_tag
def define(val=None):
    return val


@register.simple_tag
def create_list(val=None, default_value=None, *args, **kwargs):
    if val is None or val == '':
        val = default_value.split(',')
    elif isinstance(val, str):
        val = val.split(',')
    # print(val)
    return val


@register.filter
def create_default_list(val, default_value):
    if val is None or val == '':
        val = default_value.split(',')
    elif isinstance(val, str):
        val = val.split(',')
    # print(val)
    return val


@register.filter
def time_until(value):
    now = datetime.now()
    try:
        difference = value - now
    except:
        return value

    if difference <= timedelta(minutes=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}


@register.filter
def days_until(value):
    now = datetime.now(timezone.utc)
    try:
        difference = now - value
    except:
        return value

    if difference <= timedelta(days=1):
        return ''
    return ' (дни: {:d})'.format(difference.days)


@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    if qty and unit_price:
        sum = qty * unit_price
    else:
        sum = 0
    return sum


@register.simple_tag(takes_context=True)
def numworder(context, text, **kwargs):
    try:
        return num2words(text, **kwargs)
    except decimal.InvalidOperation:
        return text


@register.simple_tag
def text_currency(number, before='', curency_text='грн.', **kwargs):
    if number:
        try:
            if 'lang' not in kwargs:
                kwargs['lang'] = 'uk'
            if 'to' not in kwargs:
                kwargs['to'] = 'currency'
            if 'currency' not in kwargs:
                kwargs['currency'] = 'UAH'
            text = num2words(number, **kwargs)

            return '{:s} {:s} ({:.2f} {:s})'.format(before, text, number, curency_text)
        except decimal.InvalidOperation:
            return number
    return ''
