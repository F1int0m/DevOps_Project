from app.test.test import jsonrpc_response, url, getLoggedSession
import unittest
import requests


class AccessTests(unittest.TestCase):
    def test_NotAdminCantSeeSecretCatalog(self):
        response = requests.get(url + '/secretCatalog')
        self.assertEqual(response.status_code, 500)

        guest_session = getLoggedSession('123@c.com', '123')
        response = guest_session.get(url + '/secretCatalog')
        self.assertEqual(response.url, url + '/')

    def test_AdminCanSeeSecterCatalog(self):
        logged_session = getLoggedSession()
        response = logged_session.get(url + '/secretCatalog')
        self.assertEqual(response.status_code, 200)
