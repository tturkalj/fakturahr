# -*- coding: utf-8 -*-
import colander
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, current_app
from deform import Form, ValidationFailure, Button

from fakturahr.models.database import Session
from fakturahr.models.models import Client, Item, ClientItem
from fakturahr.views.client.validators import ClientNewValidator, ClientItemsSchema
from fakturahr.utility.helper import get_form_buttons
from fakturahr.views.helpers import get_client_list, get_item_list, get_client, get_client_items

client_view = Blueprint('client_view', __name__, url_prefix='/client')

CLIENT_NEW_ROUTE = '/new'
CLIENT_LIST_ROUTE = '/list'

CLIENT_NEW_TEMPLATE = 'client/client_new.jinja2'
CLIENT_LIST_TEMPLATE = 'client/client_list.jinja2'
CLIENT_ITEMS_TEMPLATE = 'client/client_items.jinja2'


@client_view.route(CLIENT_LIST_ROUTE)
def client_list():
    clients = get_client_list()
    context = {'client_list': clients}
    return render_template(CLIENT_LIST_TEMPLATE, **context)


@client_view.route(CLIENT_NEW_ROUTE, methods=['GET', 'POST'])
def client_new():
    if 'cancel' in request.form:
        return redirect(url_for('.client_list'))

    client_new_schema = ClientNewValidator()

    client_new_form = Form(
        client_new_schema,
        action=url_for('.client_new'),
        buttons=get_form_buttons()
    )

    if request.method == 'POST':
        try:
            controls = request.form.items(multi=True)
            appstruct = client_new_form.validate(controls)
        except ValidationFailure as e:
            current_app.logger.warning(e.error)
            template_context = {'client_new_form': client_new_form}
            return render_template(CLIENT_NEW_TEMPLATE, **template_context)

        new_client = Client(appstruct)
        Session.add(new_client)
        Session.flush()

        items = get_item_list()
        client_items_to_add = []
        for item in items:
            client_item = ClientItem(new_client.id, item.id, item.price)
            client_items_to_add.append(client_item)
        Session.add_all(client_items_to_add)
        Session.flush()

        flash(u'Uspješno ste dodali novog klijenta', 'success')
        return redirect(url_for('.client_list'))

    template_context = {
        'page_title': u'Novi klijent',
        'client_new_form': client_new_form
    }
    return render_template(CLIENT_NEW_TEMPLATE, **template_context)


@client_view.route('/edit/<int:client_id>', methods=['GET', 'POST'])
def client_edit(client_id):
    if 'cancel' in request.form:
        return redirect(url_for('.client_list'))

    client = Session.query(Client).filter(Client.id == client_id, Client.deleted == False).first()
    if not client:
        current_app.logger.warning(u'Client with id {0} not found'.format(client_id))
        flash(u'Klijent nije pronađen', 'danger')
        return redirect(url_for('.client_list'))

    client_new_schema = ClientNewValidator()
    client_new_form = Form(
        client_new_schema,
        action=url_for('.client_edit', client_id=client.id),
        appstruct=client.get_appstruct(),
        buttons=get_form_buttons()
    )

    if 'submit' in request.form:
        print request.form
        try:
            controls = request.form.items(multi=True)
            appstruct = client_new_form.validate(controls)
        except ValidationFailure as e:
            current_app.logger.warning(e.error)
            template_context = {'client_new_form': client_new_form}
            return render_template(CLIENT_NEW_TEMPLATE, **template_context)

        edited = False
        for key in appstruct:
            if hasattr(client, key):
                if appstruct[key] != colander.null:
                    if getattr(client, key) != appstruct[key]:
                        setattr(client, key, appstruct[key])
                        edited = True
                else:
                    if getattr(client, key) is not None:
                        setattr(client, key, None)
                        edited = True

        if edited:
            Session.flush()
            flash(u'Uspješno ste uredili klijenta', 'success')
        return redirect(url_for('.client_list'))

    template_context = {
        'page_title': u'Uredi klijenta',
        'client_new_form': client_new_form
    }
    return render_template(CLIENT_NEW_TEMPLATE, **template_context)


@client_view.route('/delete/<int:client_id>', methods=['GET', 'POST'])
def client_delete(client_id):
    client = get_client(client_id)
    if not client:
        current_app.logger.warning(u'Client with id {0} not found'.format(client_id))
        flash(u'Klijent nije pronađen', 'danger')
        return redirect(url_for('.client_list'))

    client.deleted = True
    for client_item in client.get_client_items():
        client_item.deleted = True

    Session.flush()

    flash(u'Uspješno ste obrisali klijenta', 'success')
    return redirect(url_for('.client_list'))


@client_view.route('/client/items/<int:client_id>', methods=['GET', 'POST'])
def client_items(client_id):
    if 'cancel' in request.form:
        return redirect(url_for('.client_list'))

    client = get_client(client_id)
    if not client:
        current_app.logger.warning(u'Client with id {0} not found'.format(client_id))
        flash(u'Klijent nije pronađen', 'danger')
        return redirect(url_for('.client_list'))

    client_items_list = get_client_items(client_id)
    client_item_ids = [client_item.id for client_item in client_items_list]

    schema = ClientItemsSchema().bind(client_item_ids=client_item_ids)
    schema['client_items'].widget.min_len = len(client_items_list)
    schema['client_items'].widget.max_len = len(client_items_list)

    appstruct = {
        'client_items': [
            {
                'client_item_id': client_item.id,
                'name': client_item.item.name,
                'price': client_item.price
            } for client_item in client_items_list
        ]
    }
    client_items_form = Form(
        schema,
        action=url_for('.client_items', client_id=client.id),
        appstruct=appstruct,
        buttons=get_form_buttons()
    )

    if request.method == 'POST':
        try:
            controls = request.form.items(multi=True)
            appstruct = client_items_form.validate(controls)
        except ValidationFailure as e:
            current_app.logger.warning(e.error)
            template_context = {
                'page_title': u'Uredi artikle klijenta',
                'client_items_form': client_items_form
            }
            return render_template(CLIENT_ITEMS_TEMPLATE, **template_context)

        edited = False
        for new_client_item in appstruct['client_items']:
            for old_client_item in client_items_list:
                if new_client_item['client_item_id'] == old_client_item.id:
                    if new_client_item['price'] != old_client_item.price:
                        old_client_item.price = new_client_item['price']
                        edited = True

        if edited:
            Session.flush()
            flash(u'Uspješno ste uredili artikle klijenta', 'success')
        return redirect(url_for('.client_list'))

    template_context = {
        'page_title': u'Uredi artikle klijenta',
        'client_items_form': client_items_form
    }
    return render_template(CLIENT_ITEMS_TEMPLATE, **template_context)


