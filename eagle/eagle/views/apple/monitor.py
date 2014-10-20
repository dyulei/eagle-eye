
#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import request
from flask import Blueprint
from urlparse import parse_qs
from eagle.views import utils
#from eagle.common import zexception
from eagle.common import http_code

monitor = Blueprint('monitor', __name__)


@monitor.route('/', methods=['GET','PUT','POST'])
@utils.controller_deco
def monitor_func(eagle_controller):
   pass


@monitor.route("/ranklist", methods=['GET'])
@utils.controller_deco
def monitor_rank_list(eagle_controller):

    query_string = parse_qs(request.query_string)

    ctrl_func = getattr(eagle_controller, '_get_monitor_rank_list')

    payload = ctrl_func(query_string)

    return payload,http_code.OK

@monitor.route("/gametype", methods=['GET'])
@utils.controller_deco
def monitor_game_type(eagle_controller):

    query_string = parse_qs(request.query_string)

    ctrl_func = getattr(eagle_controller, '_get_monitor_game_type')

    payload = ctrl_func(query_string)

    return payload,http_code.OK

@monitor.route("/companytype", methods=['GET'])
@utils.controller_deco
def monitor_company_type(eagle_controller):

    query_string = parse_qs(request.query_string)

    ctrl_func = getattr(eagle_controller, '_get_monitor_company_type')

    payload = ctrl_func(query_string)

    return payload,http_code.OK
