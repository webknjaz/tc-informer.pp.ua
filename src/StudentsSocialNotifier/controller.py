import cherrypy
from blueberrypy.template_engine import get_template
import json
import logging

logger = logging.getLogger('StudentsSocialNotifier')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/home/wk/private/kpi/4.1/pm/tc-informer.pp.ua/log/StudentsSocialNotifier.log')
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info('Running app...')

class Root:

    @cherrypy.expose
    def index(self, **kwargs):
        tmpl = get_template("index.html")
        return tmpl.render()

    @cherrypy.expose
    def list(self, **kwargs):
        tmpl = get_template("index.html")
        return tmpl.render()

    @cherrypy.expose
    def default(self, *args):
        return self.index()

class Admin:
    """administrative interface"""

    @cherrypy.expose
    def index(self, **kwargs):
        tmpl = get_template("index.html")
        return tmpl.render()

    @cherrypy.expose
    def remove(self, **kwargs):
        tmpl = get_template("index.html")
        return tmpl.render()

    @cherrypy.expose
    def add(self, **kwargs):
        tmpl = get_template("add.html")
        return tmpl.render()

    @cherrypy.expose
    def default(self, *args):
        return self.index()

class API:
    """administrative interface"""

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def index(self, **kwargs):
        logger.info('/api requested')
        tmpl = get_template("index.html")
        return tmpl.render()

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def remove(self, **kwargs):
        tmpl = get_template("index.html")
        return tmpl.render()

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def add(self, **kwargs):
        tmpl = get_template("index.html")
        return tmpl.render()

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def default(self, *args):
        return self.index()

Root.admin = Admin()
Root.api = API()
