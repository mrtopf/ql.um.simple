from ql.backend.framework import Handler, Application
from ql.backend.framework.decorators import html

import setup
import api

class App(Application):

    def setup_handlers(self, map):
        """setup the mapper"""
        with map.submapper(path_prefix=self.settings.virtual_path) as m:
            m.connect(None, '/1/users/{username}', handler=api.PoCo)
            m.connect(None, '/1/token', handler=api.Token)
    
def main():
    port = 9992
    app = App(setup.setup())
    return webserver(app, port)

def app_factory(global_config, **local_conf):
    settings = setup.setup(**local_conf)
    return App(settings)

def webserver(app, port):
    import wsgiref.simple_server
    wsgiref.simple_server.make_server('', port, app).serve_forever()

if __name__=="__main__":
    main()

