import sys
import time
import unittest
import json
from urllib import request
from urllib.error import HTTPError


class TestAPI(unittest.TestCase):
    def setUp(self):
        API_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'
        response = request.urlopen(API_URL)
        assert response.code == 200
        parsed_response = json.load(response)

        self.usd_idx = parsed_response.get('Valute').get('USD').get('Value')
        assert self.usd_idx

    def tearDown(self):
        pass

    def test_converts_correct_USD_to_RUB(self):
        multiplier = 10
        data = json.dumps({'currency': 'RUB', 'value': multiplier}).encode()
        req = request.Request(self.URL, data=data)
        resp = request.urlopen(req)
        dictionary = json.load(resp)
        result = dictionary['value'] / multiplier

        self.assertEqual(resp.code, 200)
        self.assertEqual(len(dictionary), 1)
        self.assertTrue(self.usd_idx - 1 < result < self.usd_idx + 1)

    def test_converts_correct_RUB_to_USD(self):
        multiplier = 2000
        data = json.dumps({'currency': 'USD', 'value': multiplier}).encode()
        req = request.Request(self.URL, data=data)
        resp = request.urlopen(req)
        dictionary = json.load(resp)
        result = multiplier / dictionary['value']

        self.assertEqual(resp.code, 200)
        self.assertEqual(len(dictionary), 1)
        self.assertTrue(self.usd_idx - 1 < result < self.usd_idx + 1)

    def test_returns_400_if_improper_JSON_format(self):
        data = json.dumps({'currencs': 'USD', 'value': 12}).encode()
        req = request.Request(self.URL, data=data)

        with self.assertRaises(HTTPError) as error:
            request.urlopen(req)
            self.assertEqual(error.code, 400)
            self.assertEqual(error.reason, 'Bad Request')

    def test_returns_400_if_value_field_has_str_type(self):
        data = json.dumps({'currencs': 'USD', 'value': 'asd'}).encode()
        req = request.Request(self.URL, data=data)

        with self.assertRaises(HTTPError) as error:
            request.urlopen(req)
            self.assertEqual(error.code, 400)
            self.assertEqual(error.reason, 'Bad Request')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Usage: [host:port]')

    TestAPI.URL = f'http://{sys.argv.pop()}'
    unittest.main()