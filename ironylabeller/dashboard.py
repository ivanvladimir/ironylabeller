#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# dashboard.py webApp for labelling
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


# Local imports
from forms import LoginAdmin, NewLabeller
from database import db_session
from models import Admin, Labeller

# Registering Blueprint
dashboard = Blueprint('dashboard', __name__,template_folder='ironylabeller/templates')

# Entrada a administradores
@dashboard.route("/login", methods=["GET", "POST"])
def login():
    form = LoginAdmin()
    if form.cancel.data:
        return redirect(url_for('index'))
    elif form.validate_on_submit():
        admin = Admin.query.filter(Admin.username==form.admin.data).one()
        if admin.check_passwd(form.password.data):
            admin.authenticated = True
            db_session.add(admin)
            db_session.commit()
            login_user(admin, remember=True)
            return redirect(url_for('.index'))
        else:
            return render_template("error.html", message="Nombre o password incorrecto")
    return render_template("login.html", form=form)

@dashboard.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('.login'))


@dashboard.route("/", methods=["GET", "POST"])
def index():
    ''' Entrada principal'''
    if not current_user.is_authenticated():
        return render_template('dashboard.html')
    else:
        return redirect(url_for('.login'))

@dashboard.route("/add/labeller", methods=["GET", "POST"])
def add_labeller():
    '''Agregar usuario'''
    form = NewLabeller()
    if form.cancel.data:
        return redirect(url_for('.index'))
    elif form.validate_on_submit():
        l=Labeller(form.username.data,form.password.data,form.name.data)
        db_session.add(l)
        db_session.commit()
        return redirect(url_for('.index'))
    return render_template("newlabeller.html", form=form)

