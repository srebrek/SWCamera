from splitwise import Splitwise
import urllib.parse
import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from ServiceLogic import DatabaseLogic


class Communicator:
    def __init__(self):
        self.server = HTTPServer(('localhost', 8080), RequestHandler)
        self._redirect_uri = f'http://localhost:8080'#f'http://{self.server}:{self.port}'
        self._last_request_time = 0

    def auth(self, url):
        params = {
            'response_type': 'code',
            'client_id': '',
            'redirect_uri': self._redirect_uri
        }
        request = requests.Request('GET', url, params).prepare()
        request.prepare_url(url, params)
        webbrowser.open(request.url)
        self.server.handle_request()

    def shutdown_server(self):
        self.server.shutdown()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global token
        global verifier
        self.close_connection = True
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        token = query['oauth_token']
        verifier = query['oauth_verifier']


def get():
    db = DatabaseLogic.DatabaseManager()
    db.check_is_consumer_in_db()
    consumer_key = db.get_consumer_key()
    consumer_secret = db.get_consumer_secret()
    sObj = Splitwise(consumer_key, consumer_secret)
    tempRequest = Communicator()
    url, secret = sObj.getAuthorizeURL()
    tempRequest.auth(url)
    oauth_token = token
    oauth_verifier = verifier

    access_token = sObj.getAccessToken(oauth_token[0], secret, oauth_verifier[0])
    sObj.setAccessToken(access_token)
    return sObj

