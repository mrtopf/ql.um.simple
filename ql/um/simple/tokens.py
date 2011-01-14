import uuid
import datetime

from quantumcore.storages import AttributeMapper

class Token(object):
    """a token"""

    def __init__(self, username, client_id, expires_in=3600):
        """create a new token for a user and client"""

        self.token = unicode(uuid.uuid4())
        self.refresh_token = unicode(uuid.uuid4())
        self.expires_at = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
        self.username = username
        self.client_id = client_id

    @property
    def expired(self):
        """check if this token is expired"""
        return datetime.datetime.now() < self.expires_at

    def __str__(self):
        """return a string representation"""
        return u"""<Token %s with refresh_token=%s, username=%s, client_id=%s, expires on %s>""" %(
                self.token,
                self.refresh_token,
                self.username,
                self.client_id,
                self.expires_at
                )

class Tokens(object):
    """handle OAuth tokens"""

    def __init__(self):
        """initialize the token manager"""
        self.tokens = {} # token_id => Token object
        self.refresh_tokens = {} # refresh_token -> token_id
        self.users = {} # user -> token_id
        self.clients = {} # client_id -> token_ids
    
    def create(self, client_id, username, expires_in=3600):
        """create a new token by deleting all old tokens for that user and client_id
        first. Then a new one is created and returned"""

        # delete all old tokens for that user and client
        user_token_ids = self.users.get(username, [])
        for user_token_id in user_token_ids:
            user_token = self[user_token_id]
            if user_token.client_id == client_id:
                self.delete_token(user_token)

        # create a new one
        token = Token(username, client_id, expires_in)
        self.add_token(token)
        return token

    def delete_token(self, token):
        """delete a token"""
        del self.refresh_tokens[token.refresh_token]
        del self.users[token.username]
        del self.clients[token.client_id]
        del self.tokens[token.token]

    def add_token(self, token):
        """add a new token to the database"""
        self.tokens[token.token] = token
        self.refresh_tokens[token.refresh_token] = token.token
        self.users.setdefault(token.username,[]).append(token.token)
        self.clients.setdefault(token.client_id,[]).append(token.token)


    def cleanup(self):
        """remove expired tokens"""
        for token in self.tokens.values():
            if token.expired:
                self.delete_token(token)

    def __getitem__(self, token):
        """return a token object"""
        return self.tokens.get(token,None)


class AuthManager(object):
    """the authorization manager expected by the Restful handler of ql.backend.framework"""

    def __init__(self, tokens):
        self.tokens = tokens # the token manager above

    def get(self, token):
        """retrieve a token and create some sort of user session for the request"""
        token = self.tokens[token]
        return token # for now it's the same

