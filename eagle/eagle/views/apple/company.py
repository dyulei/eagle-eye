
#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import request
from flask import Blueprint
from urlparse import parse_qs
from eagle.views import utils
#from eagle.common import zexception
from eagle.common import http_code

company = Blueprint('company',__name__)

@company.route('/ranklist', methods=['GET'])
@utils.controller_deco
def conpany_rank_list(eagle_controller):

    query_string = parse_qs(request.query_string)

    ctrl_func = getattr(eagle_controller, '_get_company_rank_list')

    payload = ctrl_func(query_string)

    return payload,http_code.OK

@company.route('/type', methods=['GET'])
@utils.controller_deco
def conpany_type(eagle_controller):

    query_string = parse_qs(request.query_string)

    ctrl_func = getattr(eagle_controller, '_get_company_type')

    payload = ctrl_func(query_string)

    return payload,http_code.OK

@company.route('/line', methods=['GET'])
@utils.controller_deco
def conpany_line(eagle_controller):

    query_string = parse_qs(request.query_string)

    ctrl_func = getattr(eagle_controller, '_get_company_line')

    payload = ctrl_func(query_string)

    return payload,http_code.OK

