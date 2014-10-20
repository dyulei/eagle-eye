#!/usr/bin/env python
# coding = utf-8

from flask import request
from flask import Blueprint
from urlparse import parse_qs
from eagle.views import utils
#from eagle.common import zexception
from eagle.common import http_code

trend = Blueprint('trend', __name__)


@trend.route('/', methods=['GET','PUT','POST'])
@utils.controller_deco
def trend_func(eagle_controller):
    pass


@trend.route("/uplist", methods=['GET'])
@utils.controller_deco
def trend_up_list(eagle_controller):
    query_string = parse_qs(request.query_string)

    ctrl_func = getattr(eagle_controller, '_get_trend_up_list')
    payload = ctrl_func(query_string)

    return payload,http_code.OK

@trend.route("/downlist", methods=['GET'])
@utils.controller_deco
def trend_down_list(eagle_controller):
    query_string = parse_qs(request.query_string)

    ctrl_func = getattr(eagle_controller, '_get_trend_down_list')
    payload = ctrl_func(query_string)

    return payload,http_code.OK

@trend.route("/uptype", methods=['GET'])
@utils.controller_deco
def trend_up_type(eagle_controller):
    query_string = parse_qs(request.query_string)

    ctrl_func = getattr(eagle_controller, '_get_trend_up_type')
    payload = ctrl_func(query_string)

    return payload,http_code.OK
@trend.route("/downtype", methods=['GET'])
@utils.controller_deco
def trend_down_type(eagle_controller):
    query_string = parse_qs(request.query_string)

    ctrl_func = getattr(eagle_controller, '_get_trend_down_type')
    payload = ctrl_func(query_string)

    return payload,http_code.OK

@trend.route("/upcompany", methods=['GET'])
@utils.controller_deco
def trend_up_company(eagle_controller):
    query_string = parse_qs(request.query_string)

    ctrl_func = getattr(eagle_controller, '_get_trend_up_company')
    payload = ctrl_func(query_string)

    return payload,http_code.OK

@trend.route("/downcompany", methods=['GET'])
@utils.controller_deco
def trend_down_company(eagle_controller):
    query_string = parse_qs(request.query_string)

    ctrl_func = getattr(eagle_controller, '_get_trend_down_company')
    payload = ctrl_func(query_string)

    return payload,http_code.OK

