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

    def test_NotAdminCantSeeSecretCatalog(self):
        response = requests.get(url + '/secretCatalog')
        self.assertEqual(response.status_code, 500)

        guestSession = getLoginedSession('123@c.com', '123')
        response = guestSession.get(url + '/secretCatalog')
        self.assertEqual(response.url, url + '/')

    def test_AdminCanSeeSecterCatalog(self):
        loginSession = getLoginedSession()
        response = loginSession.get(url + '/secretCatalog')
        self.assertEqual(response.status_code, 200)

    def test_buyNormalItemsCount(self):
        ls = getLoginedSession()
        response = buyItem(ls, 1, 1).json()
        self.assertEqual('OK', response['result'])

    def test_buyItemsTwice(self):
        ls = getLoginedSession()
        buyItem(ls, 1, 10)
        json_resp = buyItem(ls, 1, 20).json()
        self.assertEqual('OK', json_resp['result'])

    def test_incorrectBuyItems(self):
        ls = getLoginedSession()
        testCases = [[0, 1], [1, -11], [1, 'asd'], ['asd', 1]]
        for item in testCases:
            response = buyItem(ls, item[0], item[1]).json()
            self.assertEqual('Bad number', response['result']['text'])

    def test_removeFromCartAddedItem(self):
        ls = getLoginedSession()
        buyItem(ls, 1, 10)
        response = removeFromCart(ls, 1).json()
        self.assertEqual(response["result"], 'OK')

    def test_removeFromCartInvalidItem(self):
        ls = getLoginedSession()
        response = removeFromCart(ls, 'str').json()
        self.assertEqual('Bad Number', response['result']['text'])


def getLoginedSession(email='buguev.nikita@gmail.com', password='123123'):
    loginSession = requests.Session()
    payload = {'email': email, 'password': password}
    loginSession.post(url + '/login', data=payload)
    return loginSession


def buyItem(session, item_id, count):
    ids = {'item_id': item_id, 'count': count}
    return jsonrpc_response(session, 'add_to_cart', ids)


def removeFromCart(session, item_id):
    return jsonrpc_response(session, 'remove_from_cart', {'item_id': item_id})


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
