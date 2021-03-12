from jsonrpc import JSONRPCResponseManager, dispatcher
from flask import Flask, request, Blueprint

# from . import db
main = Blueprint('main', __name__)


@main.route('/profile')
def profile():
    return 'Profile'


@main.route('/', methods=['GET', 'POST'])
def index():
    return 'Help me'


@main.route('/api/health', methods=['GET', 'POST'])
def Health():
    response = Flask.response_class(
        status=200
    )
    return response


@dispatcher.add_method
def echo(input):
    return input


@main.route('/api/v1/jsonrpc', methods=['GET', 'POST'])
def application():
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Flask.response_class(
        response=response.json,
        status=200
    )
