from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO
import json


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = BytesIO()
        response.write(body)

## запуск функции
        
        res="{'lat': 'Otvet', 'lon': 'Takoy'}".encode('utf-8')
        
        self.wfile.write(res)


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
print ("Server started")
httpd.serve_forever()
