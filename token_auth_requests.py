"""An HTTP requests session for handling authentication."""

from datetime import datetime, timedelta
import requests
from requests.auth import AuthBase


class TokenAuth(AuthBase):
    """Token-based authentication.

    Parameters
    ----------
    token : str
        The authentication token.

    """

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authentication'] = 'Token {token}'.format(token=self.token)
        return r


class AuthSession:
    """An HTTP requests session which automatically handles token authentication.

    The session object exposes all the methods and fields exposed by the Session class of the requests library;
    see [1]_. Before making its first HTTP call,
    it gets an authentication token by sending the username and password to an authentication URL. The token and its
    expiry date are stored, and the token is sent in an Authentication HTTP header with all HTTP requests. If the
    token expires, a new one is requested before the next HTTO request is made.

    The username, password and token can be deleted by calling the `logout` method. You cannot make any further HTTP
    requests after doing this.

    This class is not intended for use in applications which require a high degree of security.

    Parameters
    ----------
    username : str
        The username for authentication.
    password : str
        The password for authentication.
    auth_url : str
        The URL for authenticating, i.e. for obtaining a token.

    References
    ----------
    .. [1] http://docs.python-requests.org/

    """

    http_methods = ['delete', 'get', 'head', 'options', 'patch', 'post', 'put', 'request']

    def __init__(self, username, password, auth_url):
        self._username = username
        self._password = password
        self._auth_url = auth_url
        self._token = None
        self._expiry_time = None
        self._session = requests.Session()
        self._logged_out = False

    def logout(self):
        """Remove all authentication data.

        Any attempt to make HTTP requests after calling this method will result in an AuthException being raised.

        """

        self._username = None
        self._password = None
        self._token = None
        self._expiry_time = None
        self._logged_out = True

    def __getattr__(self, item):
        """Get the item from the internal requests session, requiring a token first if need be.

        If a method corresponding to an HTTP verb is requested and there is no valid token, a token is requested from
        the authentication URL first.

        Parameters
        ----------
        item : str
            Property to return.

        Returns
        -------
        item : any
            The requested property.

        """

        session_property = getattr(self._session, item)

        if item not in AuthSession.http_methods:
            # this is not an HTTP request
            return session_property

        if self._logged_out:
            raise AuthException('No HTTP requests can be made after logging out')

        if self._has_valid_token():
            # there is a valid token
            return session_property

        self._authenticate()

        return session_property

    def _authenticate(self):
        """
        Request an authentication token and ensure it will be sent as an Authentication HTTP header.

        """

        payload = dict(username=self._username, password=self._password)
        r = requests.post(self._auth_url, json=payload)

        # handle authentication failure
        if r.status_code != 200:
            if r.status_code == 401:
                raise AuthException('Unauthorized')
            raise Exception('Unknown error')

        data = r.json()
        self._token = data['token']
        self._expiry_time = datetime.now() + timedelta(seconds=data['expires_in'])

        self._session.auth = TokenAuth(self._token)

    def _has_valid_token(self):
        return self._token and self._expiry_time and datetime.now() <= self._expiry_time - timedelta(seconds=60)


class AuthException(Exception):
    """An authentication error.

    Parameters
    ----------
    message : str
        The error message.

    """

    def __init__(self, message):
        super(Exception, self).__init__(message)


def auth_session(username, password, auth_url):
    """Create an HTTP requests session instance which automatically handles token authentication.

    This method is not intended for use in applications which require a high degree of security.

    Parameters
    ----------
    username : str
        The username for authentication.
    password : str
        The password for authentication.
    auth_url : str
        The URL for authenticating, i.e. for obtaining a token.

    Returns
    -------
    session : AuthSession
        An HTTP requests session handling token authentication.

    """

    return AuthSession(username=username, password=password, auth_url=auth_url)
