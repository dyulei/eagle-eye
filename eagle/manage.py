#!/usr/bin/env python2
# -*- encoding:utf-8 -*-

from flask import Flask
from flaskext.actions import Manager
import settings
from eagle import app

app.config.from_object(settings)
manager = Manager(app,default_server_actions=True)

if __name__ == "__main__":
    manager.run()

