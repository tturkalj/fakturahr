# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from deform import Form, ValidationFailure

from fakturahr.models.database import Session
from fakturahr.models.models import Client, Company
from fakturahr.views.client.validators import ClientNewValidator

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
    client_list = get_client_list()
    context = {'client_list': client_list}
    return render_template(CLIENT_LIST_TEMPLATE, **context)


@client_view.route(CLIENT_NEW_ROUTE, methods=['GET', 'POST'])
def client_new():
    if 'cancel' in request.form:
        return redirect(url_for('.client_list'))

    client_new_schema = ClientNewValidator()
    client_new_form = Form(client_new_schema, action=url_for('.client_new'), buttons=('submit', 'cancel'))

    if 'submit' in request.form:
        print request.form
        try:
            appstruct = client_new_form.validate(request.form.items())
        except ValidationFailure as e:
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
        flash(u'Klijent nije pronađen', 'error')
        return redirect(url_for('.client_list'))

    client_new_schema = ClientNewValidator()
    client_new_form = Form(client_new_schema,
                           action=url_for('.client_edit', client_id=client.id),
                           appstruct=client.get_appstruct(),
                           buttons=('submit', 'cancel')
                           )

    if 'submit' in request.form:
        print request.form
        try:
            appstruct = client_new_form.validate(request.form.items())
        except ValidationFailure as e:
            template_context = {'client_new_form': client_new_form}
            return render_template(CLIENT_NEW_TEMPLATE, **template_context)

        edited = client.edit_appstruct(appstruct)

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
        flash(u'Klijent nije pronađen', 'error')
        return redirect(url_for('.client_list'))

    client.deleted = True
    Session.flush()

    flash(u'Uspješno ste obrisali klijenta', 'success')
    return redirect(url_for('.client_list'))
