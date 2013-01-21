#!/usr/bin/env python3

"""
IK-92 Fileshare

CherryPy protection tool
"""

import cherrypy

#from engine.model.db import DB
#db = DB()
#db.connect()

class TrafficAlert(cherrypy.Tool):
    def __init__(self, listclass = list):
        self._point = 'on_start_resource' #or when?
        self._name = None #wtf?
        self._priority = 50 #def?
        #
        self._setargs()
        #
        self._log = {}
        #
        self._history = {}
        self.__doc__ = self.callable.__doc__
        self._struct = listclass

    def log_hit(self, path):
        log = self._log.setdefault(path, self._struct())
        log.append(time.time())

    def last_alert(self, path):
        """Returns the time of the last alert for path."""
        return self._history.get(path, 0)

    def check_alert(self, path, window, threshhold, delay, callback=None):
        # set the bar
        now = time.time()
        bar = now - window
        hits = [t for t in self._log[path] if t > bar]
        num_hits = len(hits)
        if num_hits > threshhold:
            if self.last_alert(path) + delay < now:
                self._history[path] = now
                if callback:
                    callback(path, window, threshhold, num_hits)
                else:
                    msg = '%s - %s hits within the last %s seconds.'
                    msg = msg % (path, num_hits, window)
                    cherrypy.log.error(msg, 'TRAFFIC')

    def callable(self, window = 60, threshhold = 100, delay = 30, callback = None):
        path = cherrypy.request.path_info
        self.log_hit(path)
        self.check_alert(path, window, threshhold, delay, callback)

cherrypy.tools.traffic_alert = TrafficAlert()
