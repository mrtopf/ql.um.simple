import pymongo
import logbook

from quantumcore.storages import AttributeMapper
import users
import clients
import tokens

def setup(**kw):
    """initialize the setup"""
    settings = AttributeMapper()

    settings['log'] = logbook.Logger("ql.um.simple")

    # database
    settings.db = db = pymongo.Connection().pm

    # path
    settings['virtual_path'] = ""

    # update the settings with the keywords passed in
    # TODO: enable updating of sub settings via dot notation (pm.client_id)
    settings.update(kw)

    # now setup the user store
    settings.users = users.Users(settings.user_store_filename)
    settings.clients = clients.Clients(settings.client_store_filename)
    settings.tokens = tokens.Tokens()
    settings.authmanager = tokens.AuthManager(settings.tokens)
    return settings



