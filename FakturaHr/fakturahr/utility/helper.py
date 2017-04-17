# -*- coding: utf-8 -*-
import colander
from datetime import datetime
from deform import Button

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


def get_form_buttons():
    submit = Button(name='submit', title=u'Potvrdi', type='submit', css_class='btn-primary')
    cancel = Button(name='cancel', title=u'Odustani', type='submit', css_class='btn-default')
    return submit, cancel
