import requests

import unittest

url = "http://127.0.0.1:8000"


class MainTests(unittest.TestCase):

    def test_health(self):
        response = requests.get(url + '/api/health')
        self.assertEqual(response.status_code, 200)

    def test_echo(self):
        text = 'Halp'
        response = jsonrpc_response(requests.Session(), 'echo', [text]).json()
        self.assertEqual(text, response['result'])


def getLoggedSession(email='buguev.nikita@gmail.com', password='123123'):
    logged_session = requests.Session()
    payload = {'email': email, 'password': password}
    logged_session.post(url + '/login', data=payload)
    return logged_session


def jsonrpc_response(session, method, params):
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }
    return session.post(url + '/api/v1/jsonrpc', json=payload)


if __name__ == '__main__':
    unittest.main()
