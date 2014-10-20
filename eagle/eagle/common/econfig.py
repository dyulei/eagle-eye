#!/usr/bin/python
# coding = utf-8

import yaml
import elog
import io
import os

from hashlib import md5

LOG = elog.getLogger()


def get_zconfig(file_name='config.yaml'):
    config_path = os.path.dirname(__file__)
    file_name = config_path + "/../../config/%s" % (
        file_name)
    return _load(file_name)


def _load(file_name):
    config_file = open(file_name)
    try:
        config = yaml.load(config_file)
    except:
        print "Error: config file load error,filename: %s" % file_name
        LOG.error(
            "config file %s load error,please check the config file" % file_name)
        exit(100)
    config_file.close()
    return config


