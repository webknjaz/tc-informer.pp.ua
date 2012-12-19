#!/usr/bin/env python3

"""
IK-92 Fileshare

A few helpers
"""

VK_API_SECRET = 'LABhTRDgmtQX1VErMW9J'
VK_API_ID = '3085975'

import cherrypy

def setCookie(name, value, path = '/', expires = None, max_age = 3600, version = 1):
    cherrypy.response.cookie[name] = value
    if path is not None:
        cherrypy.response.cookie[name]['path'] = path
    if expires is not None:
        cherrypy.response.cookie[key]['expires'] = expires
    if max_age is not None:
        cherrypy.response.cookie[name]['max-age'] = max_age
    if version is not None:
        cherrypy.response.cookie[name]['version'] = version

def readCookie(name):
    return cherrypy.request.cookie[name].value if name in cherrypy.request.cookie else None

def rmCookie(name):
    setCookie(name = name, value = 'expired', path = None, expires = 0, max_age = None, version = None)