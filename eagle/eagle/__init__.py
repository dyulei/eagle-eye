# -*- encoding:utf-8 -*-

import os
from settings import DEBUG
from flask import Flask
from flask import send_from_directory

from eagle.common import elog
from eagle.common import utils
from eagle.common import importutils

app = Flask(__name__)
#app.register_blueprint(frontend, url_prefix='')
LOG = elog.getLogger()
LOG.info('Flask start with name: %s' % __name__ )

url_prefix = '/eagle_eye'


if DEBUG:
    supported_blueprints = {
            'apple':['index','trend','monitor','onoff','company','app'],
            'google_play':[]
    }
else:
    supported_blueprints = utils.generate_blueprints()

for project in supported_blueprints:
    project_url_prefix=url_prefix + "/" + project
    for blueprint in supported_blueprints[project]:
        blueprint_url_prefix=project_url_prefix + "/" + blueprint
        module_name="eagle.views"+"."+project+"."+blueprint
        blueprint_module=importutils.import_module(module_name)
        blueprint_inst=getattr(blueprint_module,blueprint)
        app.register_blueprint(
                blueprint_inst,url_prefix=blueprint_url_prefix)


# router a favicon :)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')
