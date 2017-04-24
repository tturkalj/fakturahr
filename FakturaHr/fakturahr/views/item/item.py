# -*- coding: utf-8 -*-
import colander
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, current_app
from deform import Form, ValidationFailure

from fakturahr.models.database import Session
from fakturahr.models.models import Item, Client, ClientItem
from fakturahr.views.item.validators import ItemNewSchema
from fakturahr.utility.helper import get_form_buttons
from fakturahr.views.helpers import get_client_list, get_item_list, get_item

item_view = Blueprint('item_view', __name__, url_prefix='/item')

ITEM_NEW_TEMPLATE = 'item/item_new.jinja2'
ITEM_LIST_TEMPLATE = 'item/item_list.jinja2'


@item_view.route('/list', methods=['GET'])
def item_list():
    items = get_item_list()
    context = {
        'item_list': items,
        'page_title': u'Lista artikala'
    }
    return render_template(ITEM_LIST_TEMPLATE, **context)


@item_view.route('/new', methods=['GET', 'POST'])
def item_new():
    if 'cancel' in request.form:
        return redirect(url_for('.item_list'))

    item_new_schema = ItemNewSchema()
    item_new_form = Form(
        item_new_schema,
        action=url_for('.item_new'),
        buttons=get_form_buttons()
    )

    if 'submit' in request.form:
        print request.form
        try:
            appstruct = item_new_form.validate(request.form.items())
        except ValidationFailure as e:
            current_app.logger.warning(e.error)
            template_context = {'item_new_form': item_new_form}
            return render_template(ITEM_NEW_TEMPLATE, **template_context)

        new_item = Item()
        for key in appstruct:
            if hasattr(new_item, key):
                if appstruct[key] == colander.null:
                    setattr(new_item, key, None)
                else:
                    setattr(new_item, key, appstruct[key])
        Session.add(new_item)
        Session.flush()

        clients = get_client_list()
        client_items_to_add = []
        for client in clients:
            client_item = Session.query(ClientItem)\
                .filter(ClientItem.client_id == client.id,
                        ClientItem.item_id == new_item.id,
                        ClientItem.deleted == False).first()
            if not client_item:
                client_item = ClientItem(client.id, new_item.id, new_item.price)
                client_items_to_add.append(client_item)
        if client_items_to_add:
            Session.add_all(client_items_to_add)
            Session.flush()

        flash(u'Uspješno ste dodali novi artikl', 'success')
        return redirect(url_for('.item_list'))

    template_context = {
        'page_title': u'Novi artikl',
        'item_new_form': item_new_form
    }
    return render_template(ITEM_NEW_TEMPLATE, **template_context)


@item_view.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def item_edit(item_id):
    if 'cancel' in request.form:
        return redirect(url_for('.item_list'))

    item = get_item(item_id)
    if not item:
        current_app.logger.warning(u'Item with id {0} not found'.format(item_id))
        flash(u'Artikl nije pronađen', 'danger')
        return redirect(url_for('.item_list'))

    item_new_schema = ItemNewSchema()
    item_new_form = Form(
        item_new_schema,
        action=url_for('.item_edit', item_id=item.id),
        appstruct=item.get_appstruct(),
        buttons=get_form_buttons()
    )

    if 'submit' in request.form:
        try:
            appstruct = item_new_form.validate(request.form.items())
        except ValidationFailure as e:
            current_app.logger.warning(e.error)
            template_context = {'item_new_form': item_new_form}
            return render_template(ITEM_NEW_TEMPLATE, **template_context)

        edited = False
        for key in appstruct:
            if hasattr(item, key):
                if appstruct[key] != colander.null:
                    if getattr(item, key) != appstruct[key]:
                        setattr(item, key, appstruct[key])
                        edited = True
                else:
                    if getattr(item, key) is not None:
                        setattr(item, key, None)
                        edited = True

        if edited:
            Session.flush()
            flash(u'Uspješno ste uredili artikl', 'success')
        return redirect(url_for('.item_list'))

    template_context = {
        'page_title': u'Uredi artikl',
        'item_new_form': item_new_form
    }
    return render_template(ITEM_NEW_TEMPLATE, **template_context)


@item_view.route('/delete/<int:item_id>', methods=['GET', 'POST'])
def item_delete(item_id):
    item = get_item(item_id)
    if not item:
        current_app.logger.warning(u'Item with id {0} not found'.format(item_id))
        flash(u'Artikl nije pronađen', 'danger')
        return redirect(url_for('.item_list'))

    item.deleted = True

    for client_item in item.get_client_items():
        client_item.deleted = True

    Session.flush()

    flash(u'Uspješno ste obrisali artikl', 'success')
    return redirect(url_for('.item_list'))
