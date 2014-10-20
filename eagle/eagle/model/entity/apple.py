#!/usr/bin/env python
# coding = utf-8

from eagle.common import econfig

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

class AppleDB:
    def __init__(self):
        self.config=econfig.get_zconfig()
        self.generate_tables()

    def generate_tables(self):
        db=self.config.get('database')
        apple_conn=db['apple']['connection']


        engine = create_engine(apple_conn,convert_unicode=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        metadata=MetaData()
        meta=metadata
        meta.reflect(bind=engine)
        for table_name, table in meta.tables.items():
            print table_name,table
            setattr(self, table_name, table)
        session.close()
