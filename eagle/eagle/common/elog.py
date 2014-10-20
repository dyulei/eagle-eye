#!/usr/bin/env python
# coding = utf-8


import os
import sys
import syslog
import logging



log_dir = "/var/log/eagle"

if not os.path.exists(log_dir):
    os.mkdir(log_dir)


logger2=logging.getLogger()

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

handler=logging.FileHandler(log_dir+'/eagle_eye.log')
formatter = logging.Formatter('%(asctime)s %(levelname)8s %(message)s')
ch.setFormatter(formatter)
handler.setFormatter(formatter)
logger2.addHandler(handler)
logger2.addHandler(ch)
logger2.setLevel(logging.NOTSET)


def getLogger():
    return logger2

def logger(message,priority=syslog.LOG_INFO):
    '''send a message to syslog, default priority is info'''
    #logger_hdl=Pysyslog()
    #logger_hdl.syslog(message,priority=syslog.LOG_INFO)
    LOG=getLogger()
    LOG.debug(message)


if __name__ == '__main__':
    logger('test pysyslog1')
    logger('test pysyslog',syslog.LOG_DEBUG)
    LOG=getLogger()
    while True:
        LOG.debug("debug message")
        LOG.info("info message")
        LOG.warn("warn message")
        LOG.error("error message")
        LOG.critical("critical message")
