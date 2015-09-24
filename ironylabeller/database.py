#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Database for polling system for golem
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/iimas/unam
# ----------------------------------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import ConfigParser

configParser = ConfigParser.ConfigParser()
configParser.readfp(open("conf/ironylabeller.cfg"))

engine     = create_engine(configParser.get('database','DATABASE'), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)

