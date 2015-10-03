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
from flask_user import (
    login_required, UserManager, UserMixin,SQLAlchemyAdapter)
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
# Other imports
import ConfigParser

# Local import
#from user import user

# Setting the WebAPP
app = Flask('ironylabeller')
app.config.from_pyfile("../conf/ironylabeller.cfg")
mail = Mail(app) 
db = SQLAlchemy(app)

from models import User
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)


from dashboard import dashboard
from label import label
app.register_blueprint(dashboard,url_prefix='/dashboard')
app.register_blueprint(label,url_prefix='/')
