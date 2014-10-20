#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from flask import request
from flask import Blueprint
from urlparse import parse_qs
from eagle.views import utils
#from eagle.common import zexception
from eagle.common import http_code

index = Blueprint('apple_index', __name__)

@index.route('/', methods=['POST', 'DELETE', 'PUT', 'GET'])
@utils.controller_deco
def host_func(eagle_controller):
    fun = getattr(eagle_controller,'_get_control1_data')
    payload = fun()

    return payload,http_code.OK


@index.route('/month', methods=['GET'])
@utils.controller_deco
def index_month_func(eagle_controller):
    query_string = parse_qs(request.query_string)
    month_online_func = getattr(eagle_controller,'_get_month_online')
    payload = month_online_func(query_string)

    return payload,http_code.OK

@index.route('/onlinetype', methods=['GET'])
@utils.controller_deco
def index_game_type(eagle_controller,year,month):
    year = int(year)
    month = int(month)
    query_string = parse_qs(request.query_string)
    ctrl_func = getattr(eagle_controller,'_get_index_online_type')
    payload = ctrl_func(query_string)

    return payload,http_code.OK


@index.route('/day', methods=['GET'])
@utils.controller_deco
def index_day_func(eagle_controller):
    query_string = parse_qs(request.query_string)
    month_online_func = getattr(eagle_controller,'_get_day_online')
    payload = month_online_func(query_string)

    return payload,http_code.OK
# app get line with month
@index.route("/timeLineH",methods=["GET"])
@utils.controller_deco
def index_line_month(eagle_controller):
    query_string = parse_qs(request.query_string)
    if not query_string:
        return "No query string",200
    return json.dumps(query_string),200
    pass


# app get line with day
@index.route("/timeLineV",methods=["GET"])
@utils.controller_deco
def index_line_day(eagle_controller):
    query_string = parse_qs(request.query_string)
    pass

# app get online tendency
@index.route("/chartdata",methods=["GET"])
@utils.controller_deco
def index_line_tendency(eagle_controller):
    query_string = parse_qs(request.query_string)
    chart_data_func = getattr(eagle_controller,'_get_index_chart_data')
    payload = chart_data_func(query_string)

    return payload,http_code.OK
