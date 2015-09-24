#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Initialization of database for ironylabeller
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/iimas/unam
# ----------------------------------------------------------------------

from database import init_db, db_session
import sqlalchemy
import sys
import argparse
from models import Admin


if __name__ == '__main__':
    p = argparse.ArgumentParser("Author identification")
    p.add_argument("--username",default="admin",
            action="store", dest="username",
            help="Username [admin]")
    p.add_argument("--password",default="password",
            action="store", dest="passwd",
            help="Password for admin [password]")
    p.add_argument("--name",default="Admin",
            action="store", dest="name",
            help="Name [admin]")
    p.add_argument("-f","--force",default=False,
            action="store_true", dest="force",
            help="Creates new database [admin]")
 
    opts = p.parse_args()

    if not opts.force:
        try:
            adms=Admin.query.all()
            if len(adms)>0:
                print "Your database is not empty..."
                for adm in adms:
                    print ">>", adm.username, adm.name
                sys.exit(1)
                print "Use -f to force erase your full database"
        except sqlalchemy.exc.OperationalError:
            pass
  
    init_db()

    u=Admin(opts.username,opts.passwd,opts.name)
    db_session.add(u)
    db_session.commit()



