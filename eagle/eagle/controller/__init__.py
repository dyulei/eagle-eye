#!/usr/bin/env python
# coding=utf-8

from eagle.common import econfig

from eagle.controller.apple import Apple
from eagle.model import DB


class EagleController(Apple):
    """unin all model contrller together"""

    def __init__(self):
        self.set_config()
        self.set_db_inst()

    def set_config(self):
        config=econfig.get_zconfig()
        self.config=config

    def set_db_inst(self):
        self.db_inst = DB()
