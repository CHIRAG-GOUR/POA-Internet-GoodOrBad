import http.server
import socketserver

PORT = 5175

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

if __name__ == '__main__':
    # Allow address reuse to prevent 'Address already in use' errors
    socketserver.TCPServer.allow_reuse_address = True
    with ThreadingHTTPServer(("", PORT), NoCacheHTTPRequestHandler) as httpd:
        print(f"Serving at http://localhost:{PORT} (Multi-threaded, Zero-cache)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
