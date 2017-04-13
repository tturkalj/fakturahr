# -*- coding: utf-8 -*-
import colander
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from deform import Form, ValidationFailure

from fakturahr.models.database import Session
from fakturahr.models.models import Receipt, ReceiptItem
from fakturahr.views.receipt.validators import ReceiptNewValidator
from fakturahr.views.item.item import get_item_list

receipt_view = Blueprint('receipt_view', __name__, url_prefix='/receipt')

RECEIPT_NEW_TEMPLATE = 'receipt/receipt_new.jinja2'
RECEIPT_LIST_TEMPLATE = 'receipt/receipt_list.jinja2'


def get_receipt_list():
    receipts = Session.query(Receipt).filter(Receipt.deleted == False).all()
    return receipts


@receipt_view.route('/list',  methods=['GET'])
def receipt_list():
    clients = get_receipt_list()
    context = {'receipt_list': clients}
    return render_template(RECEIPT_LIST_TEMPLATE, **context)


@receipt_view.route('/new', methods=['GET', 'POST'])
def receipt_new():
    if 'cancel' in request.form:
        return redirect(url_for('.receipt_list'))

    item_list = get_item_list()

    item_id_name_list = [(item.id, item.name) for item in item_list]
    receipt_new_schema = ReceiptNewValidator().bind(items=item_id_name_list)
    receipt_new_form = Form(receipt_new_schema, action=url_for('.receipt_new'), buttons=('submit', 'cancel'))

    if 'submit' in request.form:
        print request.form
        try:
            appstruct = receipt_new_form.validate(request.form.items())
        except ValidationFailure as e:
            template_context = {'receipt_new_form': receipt_new_form}
            return render_template(RECEIPT_NEW_TEMPLATE, **template_context)

        new_receipt = Receipt()
        Session.add(new_receipt)
        Session.flush()

        flash(u'Uspješno ste dodali novi račun', 'success')
        return redirect(url_for('.receipt_list'))

    template_context = {
        'page_title': u'Novi račun',
        'receipt_new_form': receipt_new_form
    }
    return render_template(RECEIPT_NEW_TEMPLATE, **template_context)


@receipt_view.route('/edit/<int:receipt_id>', methods=['GET', 'POST'])
def receipt_edit(receipt_id):
    if 'cancel' in request.form:
        return redirect(url_for('.receipt_list'))

    receipt = Session.query(Receipt).filter(Receipt.id == receipt_id, Receipt.deleted == False).first()
    if not receipt:
        flash(u'Klijent nije pronađen', 'error')
        return redirect(url_for('.receipt_list'))

    receipt_new_schema = ReceiptNewValidator()
    receipt_new_form = Form(receipt_new_schema,
                           action=url_for('.receipt_edit', client_id=receipt.id),
                           appstruct=receipt.get_appstruct(),
                           buttons=('submit', 'cancel')
                           )

    if 'submit' in request.form:
        print request.form
        try:
            appstruct = receipt_new_form.validate(request.form.items())
        except ValidationFailure as e:
            template_context = {'receipt_new_form': receipt_new_form}
            return render_template(RECEIPT_NEW_TEMPLATE, **template_context)

        edited = False
        for key in appstruct:
            if hasattr(receipt, key):
                if appstruct[key] != colander.null:
                    if getattr(receipt, key) != appstruct[key]:
                        setattr(receipt, key, appstruct[key])
                        edited = True
                else:
                    if getattr(receipt, key) is not None:
                        setattr(receipt, key, None)
                        edited = True

        if edited:
            Session.flush()
            flash(u'Uspješno ste uredili klijenta', 'success')
        return redirect(url_for('.receipt_list'))

    template_context = {
        'page_title': u'Uredi klijenta',
        'receipt_new_form': receipt_new_form
    }
    return render_template(RECEIPT_NEW_TEMPLATE, **template_context)


@receipt_view.route('/delete/<int:receipt_id>', methods=['GET', 'POST'])
def receipt_delete(receipt_id):

    receipt = Session.query(Receipt).filter(Receipt.id == receipt_id, Receipt.deleted == False).first()
    if not receipt:
        flash(u'Račun nije pronađen', 'error')
        return redirect(url_for('.receipt_list'))

    receipt.deleted = True
    Session.flush()

    flash(u'Uspješno ste obrisali račun', 'success')
    return redirect(url_for('.receipt_list'))
