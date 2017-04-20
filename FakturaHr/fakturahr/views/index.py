# -*- coding: utf-8 -*-
import colander
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from deform import Form, ValidationFailure

from fakturahr.models.database import Session
from fakturahr.models.models import Client, Item, Receipt
from fakturahr.views.client.validators import ClientNewValidator

index_view = Blueprint('index_view', __name__)


@index_view.route('/')
def index():
    client_count = Session.query(Client).filter(Client.deleted == False).count()
    item_count = Session.query(Item).filter(Item.deleted == False).count()
    receipt_count = Session.query(Receipt).filter(Receipt.deleted == False).count()

    context = {
        'page_title': u'Početna',
        'client_count': client_count,
        'item_count': item_count,
        'receipt_count': receipt_count
    }
    return render_template('index.jinja2', **context)
