# -*- coding: utf-8 -*-
from flask import Flask
from search_engine_app.views import simple_page


def create_app(config=None):
    flask_app = Flask(__name__, static_url_path='/static')
    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.register_blueprint(simple_page)
    app.run(host='0.0.0.0')




