import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import re

YANDEX_ICS_URL = os.environ.get("YANDEX_ICS_URL", "")

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not YANDEX_ICS_URL:
            self.send_response(500)
            self.end_headers()
            self.wfile.write("YANDEX_ICS_URL not set".encode())
            return

        req = urllib.request.Request(YANDEX_ICS_URL)
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')

        data = re.sub(r'CLASS:PRIVATE', 'CLASS:PUBLIC', data)

        self.send_response(200)
        self.send_header('Content-Type', 'text/calendar; charset=utf-8')
        self.end_headers()
        self.wfile.write(data.encode('utf-8'))

    def log_message(self, format, *args):
        print(f"[{self.client_address[0]}] {format % args}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), ProxyHandler)
    print(f"Прокси запущен на порту {port}")
    server.serve_forever()
