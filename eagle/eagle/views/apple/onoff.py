#!/usr/bin/env python
# coding = utf-8

from flask import request
from flask import Blueprint
from urlparse import parse_qs
from eagle.views import utils
#from eagle.common import zexception
from eagle.common import http_code

onoff = Blueprint('onoff', __name__)


@onoff.route('/onlist', methods=['GET'])
@utils.controller_deco
def onlist_func(eagle_controller):

    query_string = parse_qs(request.query_string)
    ctrl_func = getattr(eagle_controller, '_get_online_list')
    payload = ctrl_func(query_string)

    return payload,http_code.OK

@onoff.route('/offlist', methods=['GET'])
@utils.controller_deco
def offlist_func(eagle_controller):

    query_string = parse_qs(request.query_string)
    ctrl_func = getattr(eagle_controller, '_get_offline_list')
    payload = ctrl_func(query_string)

    return payload,http_code.OK

@onoff.route('/onlist/gametype', methods=['GET'])
@utils.controller_deco
def onlist_type_func(eagle_controller):

    query_string = parse_qs(request.query_string)
    ctrl_func = getattr(eagle_controller, '_get_online_type')
    payload = ctrl_func(query_string)

    return payload,http_code.OK

@onoff.route('/offlist/gametype', methods=['GET'])
@utils.controller_deco
def offlist_type_func(eagle_controller):

    query_string = parse_qs(request.query_string)
    ctrl_func = getattr(eagle_controller, '_get_offline_type')
    payload = ctrl_func(query_string)

    return payload,http_code.OK

@onoff.route('/onlist/companytype', methods=['GET'])
@utils.controller_deco
def onlist_company_type_func(eagle_controller):

    query_string = parse_qs(request.query_string)
    ctrl_func = getattr(eagle_controller, '_get_online_company_type')
    payload = ctrl_func(query_string)

    return payload,http_code.OK

@onoff.route('/offlist/companytype', methods=['GET'])
@utils.controller_deco
def offlist_company_type_func(eagle_controller):

    query_string = parse_qs(request.query_string)
    ctrl_func = getattr(eagle_controller, '_get_offline_company_type')
    payload = ctrl_func(query_string)

    return payload,http_code.OK

