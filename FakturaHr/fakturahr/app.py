# -*- coding: utf-8 -*-
import os
from flask import Flask
from deform import Form
from deform_jinja2 import jinja2_renderer_factory
from fakturahr.views.client.client import client_view
from fakturahr.views.index import index_view
from fakturahr.views.item.item import item_view
from fakturahr.models.database import init_db


def get_root_path():
    return os.path.dirname(os.path.abspath(__file__))


def create_app(config=None):
    flask_app = Flask(__name__, template_folder='templates', static_url_path='/static')
    return flask_app


if __name__ == '__main__':
    # bootstrap_widget_templates_path = os.path.join(get_root_path(), 'templates', 'bootstrap_widget_templates')
    renderer = jinja2_renderer_factory(search_paths=['fakturahr:templates/bootstrap_widget_templates'])
    Form.set_default_renderer(renderer)
    init_db()

    app = create_app()
    app.secret_key = 'some_secret'
    app.register_blueprint(index_view)
    app.register_blueprint(client_view)
    app.register_blueprint(item_view)
    app.run(host='localhost')




