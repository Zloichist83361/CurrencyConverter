import sys
import json
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

API_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'


def request_currency(parsed_data):
    response = urllib.request.urlopen(API_URL)
    if response.code != 200:
        return None

    parsed_response = json.load(response)

    try:
        usd_idx = parsed_response.get('Valute').get('USD').get('Value')
    except AttributeError:
        return None
    else:
        if parsed_data[0] == 'RUB':
            value = round((parsed_data[1] * usd_idx), 4)
        else:
            value = round((parsed_data[1]/usd_idx), 4)

        return value


def parse_data(post_data):
    try:
        parsed_dict = json.loads(post_data)
    except json.decoder.JSONDecodeError:
        return None

    if (len(parsed_dict) != 2 or
            list(parsed_dict.keys()) != ['currency', 'value']):
        return None

    currency = parsed_dict.get('currency')
    if currency not in ('RUB', 'USD'):
        return None

    value = parsed_dict.get('value')
    if isinstance(value, (int, float)):
        return [currency, value]


class CustomHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        if post_data:
            parsed_data = parse_data(post_data)
            if parsed_data is not None:
                value = request_currency(parsed_data)

                if value is not None:
                    self.send_response(200)
                    self.send_header('content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'value': value}).encode())
                    return

        self.send_response(400)
        self.end_headers()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Expected args: [host] [port]')

    server_address = (sys.argv[1], int(sys.argv[2]))
    httpd = HTTPServer(server_address, CustomHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()