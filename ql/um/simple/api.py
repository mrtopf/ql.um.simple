import werkzeug
import urllib
try:
    import json
except ImportError:
    import simplejson as json

from ql.backend.framework import RESTfulHandler, Handler
from ql.backend.framework.decorators import html
from ql.backend.framework.decorators import json as jsonify

import errors

class Token(Handler):
    """exchanges username, password, client id and secret with an access token.
    See OAuth 2.0 Draft 11 sections 5.1.2 and 5.2 for details on how this works.

    **Allowed methods**: POST
    
    **form parameters**
    
    * ``grant_type`` (REQUIRED and MUST be 'password')
    * ``username`` (REQUIRED)
    * ``password`` (REQUIRED)
    * ``client_id`` (REQUIRED)
    * ``client_secret`` (REQUIRED)
    
    **Return value**

    If all information is correct it will return a JSON document like this::

         HTTP/1.1 200 OK
         Content-Type: application/json
         Cache-Control: no-store

         {
           "access_token":"SlAV32hkKG",
           "token_type":"example",
           "expires_in":3600,
           "refresh_token":"8xLOxBtZp8"
         }
    
    In the case of an error it will return JSON as well like this::

         HTTP/1.1 400 Bad Request
         Content-Type: application/json
         Cache-Control: no-store

         {
           "error":"invalid_request"
         }
    
    The following errors are defined:

    * ``invalid_client`` if the client id is unkown
    * ``unauthorized_client`` if the client credentials are wrong
    * ``invalid_grant`` username or password are wrong
    * ``bad_request`` if something else goes wrong, e.g. missing fields
    
    
    """
    
    def error(self, code, msg=None):
        """return an error. The code is the oauth error code to use
        and an optional message is being logged.

        TODO: return this with a 400 code and not 200!
        """

        if msg is not None:
            self.settings.log.debug("error: %s" %code)
        else:
            self.settings.log.debug("error: %s (%s)" %(code,msg))
        return {
            'error' : code,
        }

    @jsonify()
    def post(self):
        """try to authenticate the client and the user and create tokens"""
        f = self.request.form
        grant_type = f.get("grant_type", None)
        client_id = f.get("client_id", None)
        client_secret = f.get("client_secret", None)
        username = f.get("username", None)
        password = f.get("password", None)
        if grant_type is None or \
           client_id is None or\
           client_secret is None or\
           username is None or\
           password is None:
               return self.error("bad_request", "required field missing, fields passed in: %s" %f.keys())
      
        um = self.app.settings.users
        cm = self.app.settings.clients

        # check client credentials
        try:
            if not cm.check_secret(client_id, client_secret):
                return self.error("unauthorized_client")
        except errors.ClientNotFound:
            return self.error("invalid_client")

        # check user
        try:
            if not um.check_password(username, password):
                return self.error("invalid_grant")
        except errors.UserNotFound:
            return self.error("invalid_grant")

        # all credentials are ok, now create a new token and return it
        tm = self.settings.tokens
        token = tm.create(client_id, username, 3600)
        self.settings.log.debug("retrieved token %s for user %s and client %s" 
                %(token, username, client_id))

        data = {
            'access_token' : token.token,
            'refresh_token' : token.refresh_token,
            'expires_in' : 3600,
            'token_type' : 'backend'
        }
        return data


class PoCo(RESTfulHandler):
    """return a Portable Contacts record for the user identified by the token
    given.

    **Allowed methods**: GET
    
    **Return value**

    If all information is correct it will return a JSON document like this::

         HTTP/1.1 200 OK
         Content-Type: application/json

         {
            "id": 'mrtopf',
            "name": {
                "formatted": 'Christian Scholz,
            },
            "email" : 'somewhere@on.earth.com'
         }
    
    """
    
    def error(self, code, msg=None):
        """return an error. The code is the oauth error code to use
        and an optional message is being logged.

        TODO: return this with a 400 code and not 200!
        """

        if msg is not None:
            self.settings.log.debug("error: %s" %code)
        else:
            self.settings.log.debug("error: %s (%s)" %(code,msg))
        return {
            'error' : code,
        }

    @jsonify()
    def get(self, username):
        """try to authenticate the client and the user and create tokens"""
        if self.session is None:
            return self.error("invalid_token")
        username = self.session.username
        user = dict(self.settings.users.users.items(username))
        del user['password']
        user['name'] = {
            'formatted' : '%s %s' %(user['first_name'], user['last_name'])
        }
        return user


