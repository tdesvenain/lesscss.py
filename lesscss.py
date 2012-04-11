################################################################
# weishaupt.policy
# (C) 2012, ZOPYX Ltd.
################################################################

import sys
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from logger import LOG

class MyHandler(PatternMatchingEventHandler):

    def on_modified(self, event):
        path = event.src_path
        dest_path = path.replace('.less', '.css')
        cmd = 'lessc "%s" "%s"' % (path, dest_path)
        status = os.system(cmd)
        LOG.info(cmd)
        LOG.info('Status : %d' % status)

    on_created = on_modified

    def on_deleted(self, event):
        path = event.src_path
        dest_path = path.replace('.less', '.css')
        if os.path.exists(dest_path):
            LOG.info('Removed %s' % dest_path)
            os.unlink(dest_path)


    
def start():
    event_handler = MyHandler(patterns=['*.less'], ignore_directories=True)
    observer = Observer()
    path = os.path.dirname(__file__)
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    LOG.info('-'*40)
    LOG.info('Started LESSCSS watchdog')
    LOG.info('-'*40)
