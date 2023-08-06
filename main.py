from kivy.app import App
from splitwise import Splitwise
import webbrowser
import requests
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler


class Communicator:
    def __init__(self):
        self.server, self.port = 'localhost', 8080
        self._redirect_uri = f'http://{self.server}:{self.port}'
        self._last_request_time = 0

    def auth(self, url):
        #scope = ' '.join(args)

        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self._redirect_uri
        }
        request = requests.Request('GET', url, params).prepare()
        request.prepare_url(url, params)
        webbrowser.open(request.url)
        server = HTTPServer((self.server, self.port), RequestHandler)
        server.handle_request()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global token
        global verifier
        self.close_connection = True
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        token = query['oauth_token']
        verifier = query['oauth_verifier']


tempRequest = Communicator()

sObj = Splitwise('', '')
url, secret = sObj.getAuthorizeURL()
tempRequest.auth(url)
oauth_token = token
oauth_verifier = verifier

access_token = sObj.getAccessToken(oauth_token[0], secret, oauth_verifier[0])

sObj.getCurrentUser()

print('hello')
