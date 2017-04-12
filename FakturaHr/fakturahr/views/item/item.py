# -*- coding: utf-8 -*-
import colander
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from deform import Form, ValidationFailure

from fakturahr.models.database import Session
from fakturahr.models.models import Item
from fakturahr.views.item.validators import ItemNewValidator

item_view = Blueprint('item_view', __name__, url_prefix='/item')

ITEM_NEW_TEMPLATE = 'item/item_new.jinja2'
ITEM_LIST_TEMPLATE = 'item/item_list.jinja2'


def get_item_list():
    items = Session.query(Item).filter(Item.deleted == False).all()
    return items


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

    item_new_schema = ItemNewValidator()
    item_new_form = Form(item_new_schema, action=url_for('.item_new'), buttons=('submit', 'cancel'))

    if 'submit' in request.form:
        print request.form
        try:
            appstruct = item_new_form.validate(request.form.items())
        except ValidationFailure as e:
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

    item = Session.query(Item).filter(Item.id == item_id, Item.deleted == False).first()
    if not item:
        flash(u'Artikl nije pronađen', 'error')
        return redirect(url_for('.item_list'))

    item_new_schema = ItemNewValidator()
    item_new_form = Form(item_new_schema,
                         action=url_for('.item_edit', item_id=item.id),
                         appstruct=item.get_appstruct(),
                         buttons=('submit', 'cancel')
                         )

    if 'submit' in request.form:
        try:
            appstruct = item_new_form.validate(request.form.items())
        except ValidationFailure as e:
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
    item = Session.query(Item).filter(Item.id == item_id, Item.deleted == False).first()
    if not item:
        flash(u'Artikl nije pronađen', 'error')
        return redirect(url_for('.item_list'))

    item.deleted = True
    Session.flush()

    flash(u'Uspješno ste obrisali artikl', 'success')
    return redirect(url_for('.item_list'))
