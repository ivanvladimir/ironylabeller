#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ironylabeller.py Labeller for twees into ironic or not
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/IIMAS/UNAM
# ----------------------------------------------------------------------
from __future__ import print_function
from ironylabeller import app
from os.path import isfile
import argparse

if __name__ == '__main__':
    p = argparse.ArgumentParser("Author identification")
    p.add_argument("--host",default="127.0.0.1",
            action="store", dest="host",
            help="Root url [127.0.0.1]")
    p.add_argument("--port",default=5000,type=int,
            action="store", dest="port",
            help="Port url [500]")
    p.add_argument("--debug",default=False,
            action="store_true", dest="debug",
            help="Use debug deployment [Flase]")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    opts = p.parse_args()


    from ironylabeller.dashboard import dashboard
    app.register_blueprint(dashboard,url_prefix='/dashboard')
    #app.register_blueprint(user)


    app.run(debug=opts.debug,
            host=opts.host,
            port=opts.port)


