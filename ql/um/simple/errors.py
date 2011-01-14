class UserManagerError(Exception):
    """just a base class for all exceptions around the user manager"""
    
class UserNotFound(UserManagerError):
    """a user was not found in the database"""
    
    msg = "The user was not found"
    
    def __init__(self, username):
        self.username = username

class PasswordIncorrect(UserManagerError):
    """the password for the user did not match"""
    
    msg = "The password is wrong"
    
    def __init__(self, username):
        self.username = username
        
class ClientNotFound(UserManagerError):
    """exception raised if an unkown client_id is retrieved"""
    
    msg = "The client id is unkown"
    
    def __init__(self, client_id):
        """store client id in question"""
        self.client_id = client_id
        
