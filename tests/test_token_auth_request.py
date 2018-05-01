import json
import requests

from token_auth_request import auth_session


USERNAME = 'tyhuk67'
PASSWORD = 'gh37xvfkk'
TOKEN = 'x5467ghwujk78'
TOKEN_URI = 'http://www.salt.ac.za/token'
DUMMY_URI = 'http://www.salt.ac.za/'


def token_response(expires_in):
    return json.dumps(dict(token=TOKEN, expires_in=expires_in))


def test_initial_authentication_request(httpretty):
    """A token is requested before the first HTTP request."""

    httpretty.register_uri(httpretty.POST, TOKEN_URI, token_response(1000))
    httpretty.register_uri(httpretty.GET, DUMMY_URI, 'some test response')

    session = auth_session(USERNAME, PASSWORD, TOKEN_URI)
    session.get(DUMMY_URI)
    session.get(DUMMY_URI)

    # one token requst, two "normal" requests
    all_requests = httpretty.latest_requests
    assert len(all_requests) == 3

    # the first request requests a token (using POST with JSON)
    assert all_requests[0].url == TOKEN_URI
    assert all_requests[0].headers['Content-Type'] == 'application/json'
    body = json.loads(all_requests[0].body)
    assert body['username'] == USERNAME
    assert body['password'] == PASSWORD

    # the second and third request are the ones the user wants to make
    assert all_requests[1].url == DUMMY_URI
    assert all_requests[2].url == DUMMY_URI


def test_authentication_header_sent(httpretty):
    """An authentication header is sent with every request."""

    httpretty.register_uri(httpretty.POST, TOKEN_URI, token_response(1000))
    httpretty.register_uri(httpretty.GET, DUMMY_URI, 'some test response')

    session = auth_session(USERNAME, PASSWORD, TOKEN_URI)

    session.get(DUMMY_URI)
    session.get(DUMMY_URI)

    all_requests = httpretty.latest_requests
    token_header = 'Token {token}'.format(token=TOKEN)
    assert all_requests[-2].headers['Authentication'] == token_header
    assert all_requests[-1].headers['Authentication'] == token_header




