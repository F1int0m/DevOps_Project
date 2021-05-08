from app.test.test import jsonrpc_response, url, getLoggedSession
import unittest
import requests


class CartTests(unittest.TestCase):

    def test_buyNormalItemsCount(self):
        ls = getLoggedSession()
        response = buyItem(ls, 1, 1).json()
        self.assertEqual('OK', response['result'])

    def test_buyItemsTwice(self):
        ls = getLoggedSession()
        buyItem(ls, 1, 10)
        json_resp = buyItem(ls, 1, 20).json()
        self.assertEqual('OK', json_resp['result'])

    def test_incorrectBuyItems(self):
        ls = getLoggedSession()
        test_cases = [[0, 1], [1, -11], [1, 'asd'], ['asd', 1]]
        for item in test_cases:
            response = buyItem(ls, item[0], item[1]).json()
            self.assertEqual('Bad number', response['result']['text'])

    def test_removeFromCartAddedItem(self):
        ls = getLoggedSession()
        buyItem(ls, 1, 10)
        response = removeFromCart(ls, 1).json()
        self.assertEqual(response["result"], 'OK')

    def test_removeFromCartInvalidItem(self):
        ls = getLoggedSession()
        response = removeFromCart(ls, 'str').json()
        self.assertEqual('Bad Number', response['result']['text'])


def buyItem(session, item_id, count):
    ids = {'item_id': item_id, 'count': count}
    return jsonrpc_response(session, 'add_to_cart', ids)


def removeFromCart(session, item_id):
    return jsonrpc_response(session, 'remove_from_cart', {'item_id': item_id})
