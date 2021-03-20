import requests

import unittest

url = "http://127.0.0.1:8000"


class MainTests(unittest.TestCase):

    def test_health(self):
        response = requests.get(url + '/api/health')
        self.assertEqual(response.status_code, 200)

    def test_echo(self):
        text = 'Halp'
        payload = {
            "method": "echo",
            "params": [text],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(url + '/api/v1/jsonrpc', json=payload).json()
        self.assertEqual(text, response['result'])

    def test_seeSecretCatalog(self):
        response = requests.get(url + '/secretCatalog')
        self.assertEqual(response.status_code, 500)

    def test_GetSecretCatalogByAdminAcc(self):
        loginSession = requests.session()
        payload = {'email': 'buguev.nikita@gmail.com', 'password': '123123'}
        loginSession.post(url + '/login', data=payload)
        response = loginSession.get(url + '/secretCatalog')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
