#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# __init__.py webApp for labelling
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/IIMAS/UNAM
# ----------------------------------------------------------------------

# Flask imports
from flask import Flask, url_for, redirect, render_template
from flask.ext.login import LoginManager
from flask.ext.triangle import Triangle
from  flask.ext.restless import APIManager
from flask.ext.login import (
    login_user,
    logout_user,
    login_required)

# Other imports
import ConfigParser

# Local import
from dashboard import dashboard
#from user import userBB
#from info import infoB
from models import Admin, Labeller

# Setting the WebAPP
app = Flask('ironylabeller')

configParser = ConfigParser.RawConfigParser()
configParser.optionxform = str
configParser.readfp(open("conf/ironylabeller.cfg"))
app.config.update(dict(configParser._sections['webapp']))

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(dashboard,url_prefix='/dashboard')
#app.register_blueprint(userB)
#app.register_blueprint(infoB,url_prefix="/info")

@login_manager.user_loader
def load_user(userid):
    try:
        user=Labeller.query.filter(Labeller.userid==userid).one()
    except :
        try:
            user=Admin.query.get(userid)
        except:
            return None
    return user



