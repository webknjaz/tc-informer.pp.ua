import cherrypy
from blueberrypy.template_engine import get_template

class Root(object):

    @cherrypy.expose
    def index(self, **kwargs):
        tmpl = get_template("index.html")
        return tmpl.render()