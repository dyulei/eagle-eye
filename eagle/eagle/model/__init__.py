#!/usr/bin/env python
# coding = utf-8

from eagle.model.apple import Apple

from eagle.model.entity.apple import AppleDB

from eagle.common import econfig
from eagle.model.session import get_session
#from eagle.common import eexception

class DB(Apple):
    """get all model DB together"""

    def __init__(self):
        self.config = econfig.get_zconfig()
        self.generate_orm_instances()


    def get_session(self, dbtype):
        db_conn = self.config.get("database")
        conn = db_conn[dbtype]['connection']
        session = get_session(conn)

        return session

    def generate_orm_instances(self):
        try:
            self.__apple = AppleDB()
        except:
            pass
    @property
    def apple(self):
        try:
            return self.__apple
        except:
            print "hahahahahahahahahahahahahah"
            raise "Apple DB unable to connect"

