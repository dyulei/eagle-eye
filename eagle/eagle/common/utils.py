#!/usr/bin/python

'''
zeus api utils

'''
import functools
from hashlib  import md5
from hmac import HMAC
import os, re, uuid, datetime, urllib, urlparse

from SimpleAES import SimpleAES
from flask import request


import json, yaml

import sqlalchemy.engine
import sqlalchemy


def get_current_time():
    current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_time

def get_uuid():
    ''' create a uuid '''
    _uuid=uuid.uuid4()
    return _uuid

def get_x_uuid(x=None):
    uuid_prefix=x
    x_uuid=get_uuid()
    if x:
        x_uuid='%s%s' % (uuid_prefix,x_uuid)
    return x_uuid

def row2dict(row):
    d = {}
    if type(row) == sqlalchemy.engine.RowProxy:
        for column in row.items():
            column_name = column[0]
            val = column[1]
            if type(val) == datetime.datetime:
                val = str(val)
            d[column_name] = val
    elif type(row) == sqlalchemy.util._collections.NamedTuple:
        for column_name in row.keys():
            val = getattr(row, column_name)
            if type(val) == datetime.datetime:
                val = str(val)
            d[column_name] = val
    else:
        for column in row.__table__.columns:
            val = getattr(row, column.name)
            if type(val) == datetime.datetime:
                val = str(val)
            d[column.name] = val

    return d

def url_fix(s, charset='utf-8'):
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

def generate_blueprints():
    path = os.path.dirname(__file__)
    file_name = path + "/../../license"
    f = open(file_name)
    content = f.read()
    f.close()
    key = "819549b94066e84f43248454d1034188"
    aes = SimpleAES(key)
    return json.loads(aes.decrypt(content))

def md5_encrypt_password(password):
    """Hash password with md5."""

    salt = "kl7e1haz".encode('hex')

    if isinstance(password, unicode):
        password = password.encode('UTF-8')
    result = password

    for i in xrange(5):
        result = HMAC(result, salt, md5).hexdigest()
    hashed = salt + result
    return hashed

def validate_password(hashed, input_password):
    "Check input password is validate"
    if hashed == md5_encrypt_password(input_password):
        return True
    else:
        return False


def get_supported_management_zones():
    supported_management_zones = []
    path = os.path.dirname(__file__)
    config_dir = path + "/../../config/"
    files = os.listdir(config_dir)
    for f in files:
        match = re.match("mz(.*)-config.yaml", f)
        if match:
            supported_management_zones.append(match.groups()[0])
    return supported_management_zones

def get_management_zone_id(management_zone_name):
    global mzone_map
    if management_zone_name in get_supported_management_zones():
        management_zone_id = management_zone_name
    elif management_zone_name in mzone_map:
        management_zone_id = mzone_map[management_zone_name]
    else:
        management_zone_id = None

    return management_zone_id

def _get_management_zone_map():
    global supported_mzone
    management_zone_map = {}
    path = os.path.dirname(__file__)
    config_file = open(path + "/../../config/mz-map.yaml")
    config = yaml.load(config_file)
    config_file.close()

    for zone_id, zone_names in config.items():
        management_zone_map.update(
            {str(name): str(zone_id) for name in zone_names})
    return management_zone_map

#global supported_mzone, mzone_map
#supported_mzone = get_supported_management_zones()
#mzone_map = _get_management_zone_map()
