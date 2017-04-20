# -*- coding: utf-8 -*-
import colander
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, current_app
from deform import Form, ValidationFailure, Button

from fakturahr.models.database import Session
from fakturahr.models.models import Client
from fakturahr.views.client.validators import ClientNewValidator
from fakturahr.utility.helper import get_form_buttons

client_view = Blueprint('client_view', __name__, url_prefix='/client')

CLIENT_NEW_ROUTE = '/new'
CLIENT_LIST_ROUTE = '/list'

CLIENT_NEW_TEMPLATE = 'client/client_new.jinja2'
CLIENT_LIST_TEMPLATE = 'client/client_list.jinja2'


def get_client_list():
    client_list = Session.query(Client).filter(Client.deleted == False).all()
    return client_list


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

    if 'submit' in request.form:
        print request.form
        try:
            appstruct = client_new_form.validate(request.form.items())
        except ValidationFailure as e:
            current_app.logger.warning(e.error)
            template_context = {'client_new_form': client_new_form}
            return render_template(CLIENT_NEW_TEMPLATE, **template_context)

        new_client = Client(appstruct)
        Session.add(new_client)
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
            appstruct = client_new_form.validate(request.form.items())
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
    client = Session.query(Client).filter(Client.id == client_id, Client.deleted == False).first()
    if not client:
        current_app.logger.warning(u'Client with id {0} not found'.format(client_id))
        flash(u'Klijent nije pronađen', 'danger')
        return redirect(url_for('.client_list'))

    client.deleted = True
    Session.flush()

    flash(u'Uspješno ste obrisali klijenta', 'success')
    return redirect(url_for('.client_list'))
