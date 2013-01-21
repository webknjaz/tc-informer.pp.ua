#!/usr/bin/env python3

"""
IK-92 Fileshare

CherryPy protection tool
"""

import cherrypy

from ..helpers import *
from vkontakte import API, VKError, signature

import logging

logger = logging.getLogger(__name__)

def protect():
    #from engine.model.db import DB
    #db = DB()
    #db.connect()
    
    #from engine.model.user import User
    #user = User(db = db)
    
    #from ..controller import db

    #from ..controller import user
    
    try: # check VK GET/cookie here
    #if cherrypy.request.login not in users:
        #raise cherrypy.HTTPError("401 Unauthorized")
        from hashlib import md5

        #cherrypy.session['user'] = None #debug
        user = cherrypy.session.get('user')
        #logger.debug(user)
        VK = {}
        if cherrypy.session.get('user') is None or cherrypy.session['user'].get('VK') is None:
            if cherrypy.request.params.get('api_id') == VK_API_ID and md5('_'.join([cherrypy.request.params.get('api_id'), cherrypy.request.params.get('viewer_id'), VK_API_SECRET]).encode('utf8')).hexdigest() == cherrypy.request.params.get('auth_key'):
                VK = cherrypy.request.params
            elif '_'.join(['vk','app',VK_API_ID]) in cherrypy.request.cookie.keys():
                pairs = cherrypy.request.cookie['_'.join(['vk','app',VK_API_ID])].value.split('&')
                VK = {}
                for pair in pairs:
                    key, value = pair.split('=')
                    VK[key] = value
                
                if md5(''.join(['expire=', VK.get('expire'), 'mid=', VK.get('mid'), 'secret=', VK.get('secret'), 'sid=', VK.get('sid'), VK_API_SECRET]).encode('utf8')).hexdigest() == VK.get('sig'):
                    VK['viewer_id'] = VK['mid']
                else:
                    VK = {}
            else:
                #logger.debug('Authorization failed: Hacking attempt.')
                raise cherrypy.HTTPError("401 Unauthorized")#,#logger.debug('ololo'))
        
            if cherrypy.session.get('user') is None:
                cherrypy.session['user'] = {}
            if cherrypy.session['user'].get('VK') is None:
                cherrypy.session['user']['VK'] = VK
            else:
                cherrypy.session['user']['VK'].update(VK)

            # Test workaround:
            #if VK['viewer_id'] == '14135084':
            #   return
            
            if len(cherrypy.session['user']['VK']) < 1:
                return

#        if cherrypy.session['user']['VK']['viewer_id'] == '14135084':
#            return
        
        if cherrypy.session['user'].get('logout_hash') is None:
            import time
            cherrypy.session['user']['logout_hash'] = md5(str(int(time.time())).encode('utf8')).hexdigest()
        
        ##logger.debug('hash:',cherrypy.session['user']['logout_hash']) #debug
        
        #request userdetails from database
        ##logger.debug(user.get())
        
        ##logger.debug(user)


        if cherrypy.session['user'].get('logged',None) != 'in':
            from ..api import find_user_by_vk
            session = cherrypy.request.orm_session
            user = find_user_by_vk(session, cherrypy.session['user']['VK']['viewer_id'])
            #from ..model import User
            #user = cherrypy.request.orm_session.query(User).get(0)
            #logger.debug(user)
            ##logger.debug(user.full_name)
            if user:
                name_list = [user.name, user.surname]
                if user.bydad:
                    name_list.append(user.bydad)
                cherrypy.session['user'].update(user.__dict__)
                cherrypy.session['user'].update({'greeting': 'Привіт, {full_name}!'.format(full_name = ' '.join(name_list)), 'logged': 'in', 'access': 'allowed'})
            else:
                cherrypy.session['user'].update({'access': 'denied'})
        ##cherrypy.session.user = {'greeting': 'Привіт, {0}!'.format(user['VK']['viewer_id']), 'logged': 'in', 'access': 'allowed'}
        #logger.debug(cherrypy.session['user']['id'])
        if cherrypy.session['user'].get('logged',None) != 'in':
           raise cherrypy.HTTPError("401 Unauthorized")
        
        #logger.debug(cherrypy.session['user'])

    except Exception as e:
        #logger.debug('Authorization failed:', e)
        raise cherrypy.HTTPError('401 Unauthorized', 'Authorize here http://vk.com/app{API_ID}'.format(API_ID=VK_API_ID))#, IK92.error(None,code = 401))
        #pass #<irony>give it up :D</irony>

#cherrypy.tools.protect = cherrypy.Tool('on_start_resource', protect)
cherrypy.tools.protect = cherrypy.Tool('before_handler', protect)

def first_user_check():
    if cherrypy.request.path_info.startswith('/no_users'):
        return
    from ..api import get_users_list
    session = cherrypy.request.orm_session
    if get_users_list(session)['count'] < 1:
        raise cherrypy.HTTPRedirect('/no_users')

cherrypy.tools.first_user_check = cherrypy.Tool('before_handler', first_user_check)