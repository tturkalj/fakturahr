from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

simple_page = Blueprint('simple_page', __name__)


@simple_page.route('/<url_arg>/test')
def show(url_arg):
    context = {'url_arg': url_arg}
    return render_template('index.jinja2', **context)
