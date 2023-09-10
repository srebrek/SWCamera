from splitwise import Splitwise
import webbrowser
import requests
import urllib.parse
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import Models.Model.oauth_authorization_keys.splitwise_keys as splitwise_keys


class Communicator:
    def __init__(self):
        self.server, self.port = 'localhost', 8080
        self._redirect_uri = f'http://{self.server}:{self.port}'
        self._last_request_time = 0

    def auth(self, url):
        params = {
            'response_type': 'code',
            'client_id': splitwise_keys.CONSUMER_KEY,
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


def get_access_key():
    tempRequest = Communicator()

    sObj = Splitwise(splitwise_keys.CONSUMER_KEY, splitwise_keys.CONSUMER_SECRET)
    url, secret = sObj.getAuthorizeURL()
    tempRequest.auth(url)
    oauth_token = token
    oauth_verifier = verifier

    access_token = sObj.getAccessToken(oauth_token[0], secret, oauth_verifier[0])
    return access_token


def save_access_key():

    PATH = 'Models/Model/access_key.json'
    access_key = None

    if os.stat(PATH).st_size == 0:
        access_key = get_access_key()
        with open(PATH, 'w') as file:
            json.dump(access_key, file)
    else:
        with open(PATH, 'r') as file:
            access_key = json.load(file)

    return access_key
