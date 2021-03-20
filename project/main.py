from jsonrpc import JSONRPCResponseManager, dispatcher
from flask import Flask, request, Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import db, models

main = Blueprint('main', __name__)




@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, admin_flag=current_user.is_admin)


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


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



