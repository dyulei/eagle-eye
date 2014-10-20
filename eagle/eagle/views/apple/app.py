#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from flask import request
from flask import Blueprint
from urlparse import parse_qs
from eagle.views import utils
#from eagle.common import zexception
from eagle.common import http_code

app = Blueprint('apple_app', __name__)


@app.route('/lookup', methods=['GET'])
@utils.controller_deco
def app_func(eagle_controller):
    query_string = parse_qs(request.query_string)
    ctrl_func = getattr(eagle_controller,'_get_app_detail_info')
    payload = ctrl_func(query_string)
    return payload,http_code.OK

@app.route('/versionlist', methods=['GET'])
@utils.controller_deco
def version_list_func(eagle_controller):
    query_string = parse_qs(request.query_string)
    ctrl_func = getattr(eagle_controller,'_get_app_version_list')
    payload = ctrl_func(query_string)
    return payload,http_code.OK

@app.route('/chartdata', methods=['GET'])
@utils.controller_deco
def chart_data_func(eagle_controller):
    query_string = parse_qs(request.query_string)
    ctrl_func = getattr(eagle_controller,'_get_app_chart_data')
    payload = ctrl_func(query_string)
    return payload,http_code.OK
