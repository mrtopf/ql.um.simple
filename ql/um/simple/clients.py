import ConfigParser
import errors

class Clients(object):
    """imports oauth clients from a .ini-file"""

    def __init__(self,filename):
        """initialize the importer with a filename. It will automatically
        read this file and store it's contents in memory"""

        self.filename = filename
        self.clients = ConfigParser.SafeConfigParser()
        self.clients.read(filename)

    def check_secret(self, client_id, client_secret):
        """check if a secret is correct. Raises an ``ClientNotFound`` exception
        if the user is not in the database and returns ``False`` if the password does 
        not match. Otherwise it returns ``True``
        """
        try:
            if self.clients.get(client_id,"secret")!=client_secret:
                return False
        except ConfigParser.NoSectionError:
            raise errors.ClientNotFound(client_id)

        return True
        
