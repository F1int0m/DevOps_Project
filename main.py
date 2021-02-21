import requests
import json
from jsonrpc import JSONRPCResponseManager, dispatcher
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Help me'

@dispatcher.add_method
def echo(input):
    return input


@app.route('/api/health', methods=['GET', 'POST'])
def Health():
    response = app.response_class(
        status=200
    )
    return response


@app.route('/api/v1/jsonrpc', methods=['GET', 'POST'])
def application():
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return app.response_class(
        response=response.json,
        status=200
    )

if __name__ == '__main__':
    app.run(debug=True, port=8000)
