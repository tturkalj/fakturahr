# -*- coding: utf-8 -*-
import colander
from datetime import datetime


def now():
    return datetime.utcnow()


def get_number_formatted(number):
    formatted = u'{:0,.2f}'.format(number)
    formatted = formatted.replace(',', 'temp')
    formatted = formatted.replace('.', ',')
    formatted = formatted.replace('temp', '.')
    return formatted


def get_value_or_colander_null(value):
    if value is not None:
        return value
    else:
        return colander.null
