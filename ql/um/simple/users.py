import ConfigParser
import errors

class Users(object):
    """imports users from a .ini-file"""

    def __init__(self,filename):
        """initialize the importer with a filename. It will automatically
        read this file and store it's contents in memory"""

        self.filename = filename
        self.users = ConfigParser.SafeConfigParser()
        self.users.read(filename)

    def check_password(self, username, password):
        """check if a password is correct. Raises an ``UserNotFound`` exception
        if the user is not in the database and returns ``False`` if the password does 
        not match. Otherwise it returns ``True``
        """
        try:
            pw = self.users.get(username,"password")
        except ConfigParser.NoSectionError:
            raise errors.UserNotFound(username)

        if pw!=password:
            return False
       
        return True
        
