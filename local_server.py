#!/usr/bin/env python3
"""Local dev server: serves dashboards + proxies /api/ to DigitalOcean server."""
import http.server
import urllib.request
import urllib.error
import json
import os

PORT = 8080
BASE = os.path.dirname(os.path.abspath(__file__))
REMOTE_API = "http://159.65.35.217/api"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE, **kwargs)

    def do_GET(self):
        if self.path.startswith('/api/'):
            self._proxy()
        elif self.path == '/' or self.path == '/index.html':
            super().do_GET()
        elif self.path.startswith('/greenwood'):
            self.path = '/Greenwood_At_Katy/dashboard' + self.path[len('/greenwood'):]
            if self.path.endswith('/'):
                self.path += 'index.html'
            super().do_GET()
        elif self.path.startswith('/ancora'):
            self.path = '/Ancora/dashboard' + self.path[len('/ancora'):]
            if self.path.endswith('/'):
                self.path += 'index.html'
            super().do_GET()
        else:
            super().do_GET()

    def do_PUT(self):
        if self.path.startswith('/api/'):
            self._proxy()

    def do_POST(self):
        if self.path.startswith('/api/'):
            self._proxy()

    def do_OPTIONS(self):
        if self.path.startswith('/api/'):
            self._proxy()

    def _proxy(self):
        url = REMOTE_API + self.path[len('/api'):]
        body = None
        if self.headers.get('Content-Length'):
            body = self.rfile.read(int(self.headers['Content-Length']))
        req = urllib.request.Request(url, data=body, method=self.command)
        req.add_header('Content-Type', self.headers.get('Content-Type', 'application/json'))
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
                self.send_response(resp.status)
                self.send_header('Content-Type', resp.headers.get('Content-Type', 'application/json'))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            data = e.read()
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
        except urllib.error.URLError as e:
            err = json.dumps({"error": f"Cannot reach server: {e.reason}"}).encode()
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(err)
        except Exception as e:
            err = json.dumps({"error": f"Proxy error: {str(e)}"}).encode()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(err)

print(f"Local server: http://localhost:{PORT}")
print(f"  Greenwood: http://localhost:{PORT}/greenwood/")
print(f"  Ancora:    http://localhost:{PORT}/ancora/")
print(f"  API proxy -> {REMOTE_API}")
http.server.HTTPServer(('', PORT), Handler).serve_forever()
