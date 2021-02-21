import requests

import unittest

url = "http://127.0.0.1:8000"


class TestStringMethods(unittest.TestCase):

    def test1(self):
        response = requests.get(url + '/api/health')
        # print(response.status_code)
        # print('test1 end')
        self.assertEqual(response.status_code, 200)

    def test2(self):
        text = 'Halp'
        payload = {
            "method": "echo",
            "params": [text],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(url + '/api/v1/jsonrpc', json=payload).json()
        self.assertEqual(text, response['result'])


if __name__ == '__main__':
    unittest.main()
