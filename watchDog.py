#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 sagar <sagar@sagar-liquid>
#
# Distributed under terms of the GNU GPL license.

"""

"""

import pyinotify

wm = pyinotify.WatchManager() # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Creating: ", event.pathname
        
    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname
        
    def process_IN_MODIFY(self, event):
        print "Modfying:", event.pathname
        
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/home/sagar/Dropbox', mask, rec=True)
notifier.loop()
