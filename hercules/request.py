"""
request.py
"""

from http.server import BaseHTTPRequestHandler
from io import BytesIO
from requests import Request


class RequestParser(BaseHTTPRequestHandler):

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.rfile = BytesIO(self.raw_data)
        self.raw_requestline = self.rfile.readline()
        self.parse_request()

    def get_headers(self):
        return dict(self.headers)

    def get_cookies(self):
        headers = self.get_headers()
        cookies = headers.get('Cookie')
        if not cookies:
            return None
        cookies = [x.strip().split('=') for x in cookies.split(';')]
        return {x[0].strip():x[1].strip() for x in cookies}

    def get_body(self):
        data = self.raw_data.replace(b'\r', b'')
        try:
            return data[data.index(b'\n\n') + 2:].rstrip().decode('utf-8')
        except ValueError:
            return None

    def get_request(self, tls=False):
        headers = self.get_headers()
        method, query, _ = self.requestline.split(' ')

        url = f'http://{headers.get("Host")}{query}'
        return Request(method, url, data=self.get_body(), headers=headers,
            cookies=self.get_cookies())
