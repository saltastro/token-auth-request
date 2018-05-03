Quickstart
==========

This quickstart guide assumes that you have :doc:`installed <installation>` already.

Making authenticated HTTP requests
----------------------------------

Let us assume we have an API server `api.wakanda.gov.wk`, which requires token vbased authentication for its API endpoints. It expects that along with your HTTP requests you send an HTTP header of the form

.. ::code-block http

   Authentication: Token abcd1234

where `abcd1234` is the authentication token. Hopefully the token returned by the server is a bit more secure, though. Let us assume further that the server provides a route `/token`, which expects you to send an object with your username and password as a JSON string:

.. ::code-block json

   {
       "username": "tchalla",
       "password": "WakandaForever"
   }

Then you may make your life easier by using `token-auth-requests`. This package essentially provides a method `auth_session`, which accepts a username, password and the URL from which a token can be requested and returns an HTTP requests session. This session has all the functionality of a `Session` object of the `requests <http://docs.python-requests.org/>`_ library.

For example, if there is a GET route `/enemies` and a POST route `/save-the-world`, we could do the following.

.. ::code-block python

   session = auth_session(username='tchalla', password='WakandaForver', token_url='http://api.wakanda.gov.wk/token')

   # who are the enemies?
   r = session.get('http://api.wakanda.gov.wk/enemies')
   print(r.text)

   # get to work!
   r = session.post('http://api.wakanda.gov.wk/save-the-world')
   print(r.status_code)  # hopefully the status code is 200...

Refer to the `requests documentation <http://docs.python-requests.org/>`_ for all the cool stuff you can do. You don't have to worry about about tokens or their expiry dates; they are taken care of automatically.

When things go boom in the night
--------------------------------

If you try to authenticate with a wrong username or password (and the server does the right thing and responds with a 401 status code), an `AuthException` is raised.

.. ::code-block python

   try:
       session = auth_session(username='tchalla', password='WakandaIsLost', token_url='http://api.wakanda.gov.wk/token')
   except AuthException as ae:
       print(ae.message)

In case the server replies with a status code other than 200 (OK) or 401 (Unauthorized), a more generic exception is raised.


