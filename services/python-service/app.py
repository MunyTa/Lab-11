import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        if self.path == '/health':
            return
        super().log_message(format, *args)

def run_server():
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"Server running on port {port}, debug={debug}")
    
    if debug:
        print("Debug mode enabled - logging active")
        Handler.log_message = lambda self, format, *args: print(format % args)
    
    server.serve_forever()

if __name__ == '__main__':
    run_server()