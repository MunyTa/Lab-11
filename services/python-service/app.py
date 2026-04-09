import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # TODO: Реализовать правильно
        if self.path == '/health':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"{}")
        elif self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Wrong response")
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    port = int(os.getenv('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"Server running on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    run_server()