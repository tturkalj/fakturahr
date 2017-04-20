# -*- coding: utf-8 -*-
import colander
import json
from io import BytesIO
from deform import Form, ValidationFailure
from datetime import datetime
from tempfile import NamedTemporaryFile
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, send_file, current_app
from fakturahr.models.database import Session
from fakturahr.models.models import Receipt, ReceiptItem, Item, User
from fakturahr.views.receipt.validators import ReceiptNewValidator
from fakturahr.views.item.item import get_item_list, get_item
from fakturahr.views.client.client import get_client_list
from fakturahr.utility.helper import get_value_or_colander_null, get_form_buttons
from fakturahr.utility.receipt_export import get_receipt_document

receipt_view = Blueprint('receipt_view', __name__, url_prefix='/receipt')

RECEIPT_NEW_TEMPLATE = 'receipt/receipt_new.jinja2'
RECEIPT_LIST_TEMPLATE = 'receipt/receipt_list.jinja2'


def get_receipt_list():
    receipts = Session.query(Receipt).filter(Receipt.deleted == False).all()
    return receipts


@receipt_view.route('/list',  methods=['GET'])
def receipt_list():
    receipts = get_receipt_list()
    context = {
        'receipt_list': receipts,
        'page_title': u'Lista računa'
    }
    return render_template(RECEIPT_LIST_TEMPLATE, **context)


@receipt_view.route('/new', methods=['GET', 'POST'])
def receipt_new():
    if 'cancel' in request.form:
        return redirect(url_for('.receipt_list'))

    item_list = get_item_list()
    item_data_list = [
        {
            'id': item.id,
            'name': item.get_name(),
            'ean': item.get_ean(),
            'measurement_unit': item.get_measurement_unit(),
            'price': item.get_price_float(),
            'price_formatted': item.get_price_formatted(),
            'return_amount': item.get_return_amount()
        } for item in item_list
    ]

    item_id_name_list = [(item.id, item.name) for item in item_list]
    item_id_name_list.insert(0, ('', '-Odaberi artikl-'))

    client_list = get_client_list()
    client_id_name_list = [(client.id, client.get_name()) for client in client_list]
    client_id_name_list.insert(0, ('', '-Odaberi klijenta-'))

    payment_types = [(payment_type, payment_name)
                     for payment_type, payment_name in Receipt.get_payment_option_dict().iteritems()]

    receipt_new_schema = ReceiptNewValidator().bind(
        items=item_id_name_list,
        item_data_list=json.dumps(item_data_list),
        clients=client_id_name_list,
        payment_types=payment_types
    )

    default_user = Session.query(User).filter(User.firstname == u'Miroslav').first()
    appstruct = {
        'operator': u'{0} {1}'.format(default_user.firstname, default_user.lastname),
    }

    receipt_new_form = Form(
        receipt_new_schema,
        action=url_for('.receipt_new'),
        buttons=get_form_buttons(),
        formid='receipt-new-form',
        appstruct=appstruct
    )

    template_context = {
        'page_title': u'Novi račun',
        'receipt_new_form': receipt_new_form,
        'item_data_list': json.dumps(item_data_list),
        'tax_percent': Receipt.TAX_PERCENT,
    }

    if 'submit' in request.form:
        try:
            controls = request.form.items(multi=True)
            appstruct = receipt_new_form.validate(controls)
        except ValidationFailure as e:
            current_app.logger.warning(e.error)
            return render_template(RECEIPT_NEW_TEMPLATE, **template_context)

        new_receipt = Receipt()
        new_receipt.tax_percent = Receipt.TAX_PERCENT
        new_receipt.user_id = default_user.id
        for key in appstruct:
            if hasattr(new_receipt, key):
                if key in ('issued_date', 'currency_date'):
                    parsed_date = datetime.strptime(appstruct[key], Receipt.date_format)
                    setattr(new_receipt, key, parsed_date)
                elif key == 'payment_type':
                    setattr(new_receipt, key, Receipt.SLIP)
                else:
                    setattr(new_receipt, key, appstruct[key])
        Session.add(new_receipt)
        Session.flush()

        added_receipt_items_list = []
        for item in appstruct['receipt_items']:
            item_object = get_item(item['item_id'])
            item_object.stock_quantity -= item['quantity']

            new_receipt_item = ReceiptItem()
            new_receipt_item.receipt_id = new_receipt.id
            new_receipt_item.name = item_object.name
            for key in item:
                if hasattr(new_receipt_item, key):
                    setattr(new_receipt_item, key, item[key])

            added_receipt_items_list.append(new_receipt_item)
        Session.add_all(added_receipt_items_list)
        Session.flush()

        flash(u'Uspješno ste dodali novi račun', 'success')
        return redirect(url_for('.receipt_list'))

    return render_template(RECEIPT_NEW_TEMPLATE, **template_context)


@receipt_view.route('/edit/<int:receipt_id>', methods=['GET', 'POST'])
def receipt_edit(receipt_id):
    if 'cancel' in request.form:
        return redirect(url_for('.receipt_list'))

    receipt = Session.query(Receipt).filter(Receipt.id == receipt_id, Receipt.deleted == False).first()
    if not receipt:
        current_app.logger.warning(u'Receipt with id {0} not found'.format(receipt_id))
        flash(u'Račun nije pronađen', 'danger')
        return redirect(url_for('.receipt_list'))

    item_list = get_item_list()
    item_data_list = [
        {
            'id': item.id,
            'name': item.get_name(),
            'ean': item.get_ean(),
            'measurement_unit': item.get_measurement_unit(),
            'price': item.get_price_float(),
            'price_formatted': item.get_price_formatted(),
            'return_amount': item.get_return_amount()
        } for item in item_list
    ]

    item_id_name_list = [(item.id, item.name) for item in item_list]
    item_id_name_list.insert(0, ('', '-Odaberi artikl-'))

    client_list = get_client_list()
    client_id_name_list = [(client.id, client.get_name()) for client in client_list]
    client_id_name_list.insert(0, ('', '-Odaberi klijenta-'))

    payment_types = [(payment_type, payment_name)
                     for payment_type, payment_name in Receipt.get_payment_option_dict().iteritems()]

    receipt_new_schema = ReceiptNewValidator().bind(
        items=item_id_name_list,
        item_data_list=json.dumps(item_data_list),
        clients=client_id_name_list,
        payment_types=payment_types
    )

    default_user = Session.query(User).filter(User.firstname == u'Miroslav').first()

    appstruct = {
        'client_id': receipt.client_id,
        'number': receipt.number,
        'issued_date': receipt.issued_date.strftime(receipt.date_format),
        'currency_date': receipt.currency_date.strftime(receipt.date_format),
        'issued_time': get_value_or_colander_null(receipt.issued_time),
        'issued_location': get_value_or_colander_null(receipt.issued_location),
        'tax_percent': get_value_or_colander_null(receipt.tax_percent),
        'base_amount': get_value_or_colander_null(receipt.base_amount),
        'tax_amount': get_value_or_colander_null(receipt.tax_amount),
        'return_amount': get_value_or_colander_null(receipt.return_amount),
        'total_amount': get_value_or_colander_null(receipt.total_amount),
        'operator': u'{0} {1}'.format(default_user.firstname, default_user.lastname),
        'payment_type': get_value_or_colander_null(receipt.payment_type),
        'receipt_items': [{
            'item_id': receipt_item.item_id,
            'ean': get_value_or_colander_null(receipt_item.ean),
            'measurement_unit': get_value_or_colander_null(receipt_item.measurement_unit),
            'quantity': get_value_or_colander_null(receipt_item.quantity),
            'rebate_percent': get_value_or_colander_null(receipt_item.rebate_percent),
            'item_price': get_value_or_colander_null(receipt_item.item_price),
            'item_price_sum': get_value_or_colander_null(receipt_item.item_price_sum),
        } for receipt_item in receipt.items]
    }

    receipt_new_form = Form(
        receipt_new_schema,
        action=url_for('.receipt_edit', receipt_id=receipt.id),
        buttons=get_form_buttons(),
        formid='receipt-new-form',
        appstruct=appstruct
    )

    template_context = {
        'page_title': u'Uredi račun',
        'receipt_new_form': receipt_new_form,
        'item_data_list': json.dumps(item_data_list),
        'tax_percent': receipt.tax_percent,
    }

    if 'submit' in request.form:
        try:
            controls = request.form.items(multi=True)
            appstruct = receipt_new_form.validate(controls)
        except ValidationFailure as e:
            current_app.logger.warning(e.error)
            template_context = {'receipt_new_form': receipt_new_form}
            return render_template(RECEIPT_NEW_TEMPLATE, **template_context)

        edited = False
        for key in appstruct:
            if hasattr(receipt, key) and key not in ('payment_type'):
                if appstruct[key] != colander.null:
                    if key in ('issued_date', 'currency_date'):
                        parsed_date = datetime.strptime(appstruct[key], Receipt.date_format)
                        if getattr(receipt, key) != parsed_date:
                            setattr(receipt, key, parsed_date)
                            edited = True
                    else:
                        if getattr(receipt, key) != appstruct[key]:
                            setattr(receipt, key, appstruct[key])
                            edited = True
                else:
                    if getattr(receipt, key) is not None:
                        setattr(receipt, key, None)
                        edited = True

        receipt_items_indexed = receipt.get_receipt_items_indexed()
        appstruct_receipt_items_indexed = {index: item for index, item in enumerate(appstruct['receipt_items'])}
        for index, receipt_item in receipt_items_indexed.iteritems():
            if index not in appstruct_receipt_items_indexed:
                receipt_item.deleted = True
                edited = True
            else:
                appstruct_receipt_item = appstruct_receipt_items_indexed[index]
                for key in appstruct_receipt_item:
                    if hasattr(receipt_item, key):
                        if appstruct_receipt_item[key] != colander.null:
                            if appstruct_receipt_item[key] != getattr(receipt_item, key):
                                item_object = get_item(appstruct_receipt_item['item_id'])
                                if key == 'item_id':
                                    receipt_item.name = item_object.name
                                elif key == 'quantity':
                                    quantity_delta = receipt_item.quantity - appstruct_receipt_item['quantity']
                                    item_object.stock_quantity += quantity_delta
                                setattr(receipt_item, key, appstruct_receipt_item[key])
                                edited = True
                        else:
                            if getattr(receipt_item, key) is not None:
                                setattr(receipt_item, key, None)
                                edited = True

        for index, appstruct_receipt_item in appstruct_receipt_items_indexed.iteritems():
            if index not in receipt_items_indexed:
                item_object = Session.query(Item).filter(Item.id == appstruct_receipt_item['item_id'],
                                                         Item.deleted == False).first()

                item_object.stock_quantity -= appstruct_receipt_item['quantity']

                new_receipt_item = ReceiptItem()
                new_receipt_item.receipt_id = receipt.id
                new_receipt_item.name = item_object.name
                for key in appstruct_receipt_item:
                    if hasattr(new_receipt_item, key):
                        setattr(new_receipt_item, key, appstruct_receipt_item[key])
                edited = True
                Session.add(new_receipt_item)
                Session.flush()

        if edited:
            Session.flush()
            flash(u'Uspješno ste uredili račun', 'success')
        return redirect(url_for('.receipt_list'))

    return render_template(RECEIPT_NEW_TEMPLATE, **template_context)


@receipt_view.route('/delete/<int:receipt_id>', methods=['GET', 'POST'])
def receipt_delete(receipt_id):

    receipt = Session.query(Receipt).filter(Receipt.id == receipt_id, Receipt.deleted == False).first()
    if not receipt:
        current_app.logger.warning(u'Receipt with id {0} not found'.format(receipt_id))
        flash(u'Račun nije pronađen', 'danger')
        return redirect(url_for('.receipt_list'))

    receipt.deleted = True
    for receipt_item in receipt.items:
        receipt_item.deleted = True
    Session.flush()

    flash(u'Uspješno ste obrisali račun', 'success')
    return redirect(url_for('.receipt_list'))


@receipt_view.route('/export/<int:receipt_id>', methods=['GET'])
def receipt_export(receipt_id):
    receipt = Session.query(Receipt).filter(Receipt.id == receipt_id, Receipt.deleted == False).first()
    if not receipt:
        current_app.logger.warning(u'Receipt with id {0} not found'.format(receipt_id))
        flash(u'Račun nije pronađen', 'danger')
        return redirect(url_for('.receipt_list'))

    receipt_document = get_receipt_document(receipt)

    with NamedTemporaryFile(suffix=u'.docx', delete=True) as temp_file:
        try:
            receipt_document.save(temp_file)
        except Exception as e:
            flash(u'Greška kod generiranja računa', 'danger')
            return redirect(url_for('.receipt_list'))

        temp_file.seek(0)
        byteio = BytesIO()
        byteio.write(temp_file.read())
        byteio.seek(0)

    attachment_name = u'Račun-{0}.docx'.format(receipt.get_number()).encode(u'utf-8')

    return send_file(byteio, as_attachment=True, attachment_filename=attachment_name)
