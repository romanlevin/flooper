from flask import Blueprint


flooper_ui = Blueprint('flooper_ui', __name__)


@flooper_ui.route('/')
def index():
    return u'Hello World!'
