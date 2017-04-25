# -*- coding: utf-8 -*-
import config
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, Request, request, current_app
from werkzeug.datastructures import OrderedMultiDict
from deform import Form
from deform_jinja2 import jinja2_renderer_factory
from fakturahr.views.client.client import client_view
from fakturahr.views.index import index_view
from fakturahr.views.item.item import item_view
from fakturahr.views.receipt.receipt import receipt_view
from fakturahr.models.database import init_models, Session
from fakturahr.utility.init_db import init_db
from fakturahr import get_root_path


class AppRequest(Request):
    parameter_storage_class = OrderedMultiDict


def create_app(config=None):
    flask_app = Flask(__name__, template_folder='templates', static_url_path='/static')
    flask_app.request_class = AppRequest
    flask_app.secret_key = 'some_secret'
    flask_app.register_blueprint(index_view)
    flask_app.register_blueprint(client_view)
    flask_app.register_blueprint(item_view)
    flask_app.register_blueprint(receipt_view)
    return flask_app


# def log_request_info():
#     current_app.logger.debug(u'Headers: %s', request.headers)
#     current_app.logger.debug(u'Body: %s', request.get_data())
#     print 'logging..'


if __name__ == '__main__':
    # bootstrap_widget_templates_path = os.path.join(get_root_path(), 'templates', 'bootstrap_widget_templates')
    renderer = jinja2_renderer_factory(search_paths=['fakturahr:templates/bootstrap_widget_templates'])
    Form.set_default_renderer(renderer)
    init_models()

    init_db()

    app = create_app()

    log_handler = TimedRotatingFileHandler(
        filename=os.path.join(get_root_path(), config.LOG_FILE_PATH),
        when='midnight',
        backupCount=365
    )
    formatter = logging.Formatter(u'[%(asctime)s] {%(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)

    app.logger.setLevel(logging.DEBUG)

    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.ERROR)

    @app.before_request
    def log_request_info():
        app.logger.debug(u'Route {0}; Request params: {1}'.format(request.path, request.values))

    app.run(host='localhost', debug=False)
