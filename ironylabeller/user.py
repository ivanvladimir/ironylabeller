#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# user.py webApp for labelling
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/IIMAS/UNAM
# ----------------------------------------------------------------------

# Flask imports
from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    request,
    make_response, 
    current_app
    )
from flask.ext.login import (
    login_user,
    logout_user,
    current_user,
    login_required)
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

# Local imports
from forms import LoginLabeller, NewLabeller, EditLabeller
from database import db_session
from models import Admin, Labeller, Task

# Registering Blueprint
user = Blueprint('user', __name__,template_folder='ironylabeller/templates')

# Entrada a administradores
@user.route("/login", methods=["GET", "POST"])
def login():
    form = LoginLabeller()
    if form.cancel.data:
        return redirect(url_for('.login'))
    elif form.validate_on_submit():
        user = Labeller.query.filter(Labeller.username==form.username.data).one()
        if user.check_passwd(form.passwd.data):
            user.authenticated = True
            db_session.add(user)
            db_session.commit()
            login_user(user, remember=True)
            return redirect(url_for('.index'))
        else:
            return render_template("error.html", message="Nombre o password incorrecto")
    return render_template("login_user.html", form=form)

@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('.login'))


@user.route("/", methods=["GET", "POST"])
@login_required
def label():
    ''' Label'''
    return "label"

@user.route("/", methods=["GET", "POST"])
def index():
    ''' Entrada principal'''
    if not current_user.is_authenticated():
        return redirect(url_for('.label'))
    else:
        return redirect(url_for('.login'))
