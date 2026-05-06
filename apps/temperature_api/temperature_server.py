from http.server import HTTPServer, BaseHTTPRequestHandler
import random

MINIMUM_TEMPERATURE = 15

class Serv(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
    
    def do_GET(self):
        if self.path.startswith("/temperature"):
            rnd_temperature = random.random() * 10 + MINIMUM_TEMPERATURE
            self._set_response()
            self.wfile.write("{:.2f}".format(rnd_temperature).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

httpd = HTTPServer(('0.0.0.0', 8081), Serv)
httpd.serve_forever()

