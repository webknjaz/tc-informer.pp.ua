import cherrypy
from blueberrypy.template_engine import get_template
import json
import logging

logger = logging.getLogger(__name__)

from .tools import *

#MENU_LIST = [
#    {'id': 'users_list', 'name': 'Юзери', 'url': '/'},
#    {'id': 'no_users', 'name': 'Нема', 'url': '/no_users'},
#    {'id': 'logged_in', 'name': 'Зайшов', 'url': '/logged_in'},
#    {'id': 'add_user', 'name': 'Додати', 'url': '/admin/add'}
#]

MENU_LIST = [
    {'id': 'users_list', 'name': 'Users List', 'url': '/list'},
    {'id': 'no_users', 'name': 'No users in system', 'url': '/no_users'},     # DEBUG item
    {'id': 'logged_in', 'name': 'Logged in', 'url': '/logged_in'}, # DEBUG item
    {'id': 'add_user', 'name': 'Manage users', 'url': '/admin'}
]

#def menu_item(fn, *args, **kwargs):
#    def wrapped(fn, *wargs, **wkwargs):
#        if len(args) > 0:
#            fn.menu_item = args[0]
#        fn.menu_item = 'trololo'
        #self.get(fn)
#        return 'lololo'
#        return fn
#    return wrapped
#    return 'olololo'

class Root:

    #@menu_item('users_list')
    @cherrypy.expose(alias = 'list')
    def index(self, **kwargs):
        # VK args list:
        #   hash, api_url, auth_key, referrer, access_token,
        #   is_app_user, api_id, viewer_id, language, secret, sid,
        #   lc_name, user_id, group_id, api_settings, ad_info,
        #   parent_language, viewer_type
        # from .api import get_users_list
        # session = cherrypy.request.orm_session
        # users = get_users_list(session)
        # tmpl = get_template("index.html")
        # return tmpl.render(menu_items = MENU_LIST, menu_item = 'users_list', users = users['list'])
        #from .api import get_users_list
        #session = cherrypy.request.orm_session
        #users = get_users_list(session)
        tmpl = get_template("index.html")
        #return tmpl.render(menu_items = MENU_LIST, menu_item = 'users_list', users = users['list'])
        return tmpl.render(menu_items = MENU_LIST, menu_item = 'users_list')

    @cherrypy.expose
    def logged_in(self, **kwargs):
        tmpl = get_template("logged_in.html")
        logger.debug(cherrypy.session)
        logger.debug(cherrypy.session.__dict__)
        logger.debug(cherrypy.session.get('user'))
        return tmpl.render(user = cherrypy.session['user'], menu_items = MENU_LIST, menu_item = 'logged_in')

    @cherrypy.expose
    def no_users(self, **kwargs):
        from .api import get_users_list
        session = cherrypy.request.orm_session
        if not get_users_list(session)['count']:
            raise cherrypy.HTTPRedirect('/')
        tmpl = get_template("no_users.html")
        return tmpl.render(menu_items = MENU_LIST, menu_item = 'no_users')

    @cherrypy.expose
    def default(self, *args):
        tmpl = get_template("access_denied.html")
        return tmpl.render()

    @cherrypy.expose
    def admin(self, **kwargs):
        from .api import get_users_list
        session = cherrypy.request.orm_session
        users = get_users_list(session)
        tmpl = get_template("add.html")
#        pagination = []
#        if kwargs.get('start') and kwargs.get('start') < 20:
#            pagination.append({'id': kwargs.get('start') - 20, 'name': 'Prev', 'url': '/'})
#        pagination = users['count'] if users['count'] > 20 else None
        return tmpl.render(menu_items = MENU_LIST, menu_item = 'add_user', users = users['list'])

#class Admin:
#    """administrative interface"""

#    @cherrypy.expose
#    def index(self, **kwargs):
#        tmpl = get_template("index.html")
#        return tmpl.render(menu_items = MENU_LIST, menu_item = 'users_list')

#    @cherrypy.expose
#    def remove(self, **kwargs):
#        tmpl = get_template("index.html")
#        return tmpl.render(menu_items = MENU_LIST, menu_item = 'users_list')

#    @cherrypy.expose
#    def add(self, **kwargs):
#        from .api import get_users_list
#        session = cherrypy.request.orm_session
#        users = get_users_list(session)
#        tmpl = get_template("add.html")
#        pagination = []
#        if kwargs.get('start') and kwargs.get('start') < 20:
#            pagination.append({'id': kwargs.get('start') - 20, 'name': 'Prev', 'url': '/'})
#        pagination = users['count'] if users['count'] > 20 else None
#        return tmpl.render(menu_items = MENU_LIST, menu_item = 'add_user', users = users['list'])

#    @cherrypy.expose
#    def default(self, *args):
#        return self.index()

@cherrypy.tools.json_out()
class API:
    """administrative interface"""

    @cherrypy.expose
    def index(self, **kwargs):
        logger.info('/api requested')
        return {'status': 'error', 'error_id': 403, 'msg': 'Access restricted: This API is private.'}

    @cherrypy.expose
    def remove(self, uid, **kwargs):
        #assert cherrypy.request.method == 'POST', 'POST queries are only accepted'
        ret_obj = None
        try:
            from .api import delete_user_by_id
            session = cherrypy.request.orm_session
            res = delete_user_by_id(session, id = uid)
            ret_obj = {
                        'status': 'ok', 
                        'msg': 'User removed successfully!', 
                        'user_id': uid
            }
        except:
            ret_obj = {
                        'status': 'fail',
                        'msg': 'This VK user does not exist.'
                        }
        return ret_obj

    @cherrypy.expose
    def add(self, name, surname, bydad = None, vk_link = None, **kwargs):
        #assert cherrypy.request.method == 'POST', 'POST queries are only accepted'
        ret_obj = None
        try:
            from .api import add_user
            session = cherrypy.request.orm_session
            user = add_user(session, name = name, surname = surname, bydad = bydad, vk_id = vk_link)
            nl = [user.surname, user.name]
            if user.bydad:
                nl.append(user.bydad)
            ret_obj = {
                        'status': 'ok', 
                        'msg': 'User added successfully!', 
                        'user': {
                                'id': user.id, 
                                'name': ' '.join(nl)
                                }
            }
        except:
            ret_obj = {
                        'status': 'fail',
                        'msg': 'This VK user exists.'
                        }
        return ret_obj

    @cherrypy.expose
    def add_admin(self, name, surname, bydad = None, **kwargs):
        #assert cherrypy.request.method == 'POST', 'POST queries are only accepted'
        ret_obj = None
        try:
            from .api import add_first_user
            session = cherrypy.request.orm_session
            user = add_first_user(session, name = name, surname = surname, bydad = bydad)
            nl = [user.surname, user.name]
            if user.bydad:
                nl.append(user.bydad)
            ret_obj = {
                        'status': 'ok', 
                        'msg': 'User added successfully!', 
                        'user': {
                                'id': user.id, 
                                'name': ' '.join(nl)
                                }
                        }
        except AssertionError:
            ret_obj = {
                        'status': 'fail',
                        'msg': 'Admin exists.'
                        }
        return ret_obj

    @cherrypy.expose
    def default(self, *args):
        return {'status': 'error', 'error_id': 404, 'msg': 'This URL is not accessible!'}
        #return self.index()

#Root.admin = Admin()
Root.api = API()
