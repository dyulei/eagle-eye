#!/usr/bin/python


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

global _MAKERS
_MAKERS = {}

def get_session(connection,autocommit=False, expire_on_commit=False):
    global _MAKERS
    if not _MAKERS.has_key(connection):
        connection += "?charset=utf8"
        engine = create_engine(connection,convert_unicode=True)
        _MAKERS[connection] = sessionmaker(bind=engine,
                               autocommit=autocommit,
                               expire_on_commit=expire_on_commit)
    maker = _MAKERS[connection]
    session = maker()
    return session

