# -*- coding: utf-8 -*-
import os
from flask import Flask, Request
from werkzeug.datastructures import OrderedMultiDict
from deform import Form
from deform_jinja2 import jinja2_renderer_factory
from fakturahr.views.client.client import client_view
from fakturahr.views.index import index_view
from fakturahr.views.item.item import item_view
from fakturahr.views.receipt.receipt import receipt_view
from fakturahr.models.database import init_models, Session
from fakturahr.utility.init_db import init_db


class AppRequest(Request):
    parameter_storage_class = OrderedMultiDict


def create_app(config=None):
    flask_app = Flask(__name__, template_folder='templates', static_url_path='/static')
    flask_app.request_class = AppRequest
    return flask_app


if __name__ == '__main__':
    # bootstrap_widget_templates_path = os.path.join(get_root_path(), 'templates', 'bootstrap_widget_templates')
    renderer = jinja2_renderer_factory(search_paths=['fakturahr:templates/bootstrap_widget_templates'])
    Form.set_default_renderer(renderer)
    init_models()

    init_db()

    app = create_app()

    app.secret_key = 'some_secret'
    app.register_blueprint(index_view)
    app.register_blueprint(client_view)
    app.register_blueprint(item_view)
    app.register_blueprint(receipt_view)
    app.run(host='localhost')




