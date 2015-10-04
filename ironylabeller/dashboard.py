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
from flask_user import (
    login_required,
    roles_accepted)
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from ironylabeller import user_manager, db

# Local imports
from forms import NewUser, EditLabeller
from models import User, Task, Role, Labelling

# Registering Blueprint
dashboard = Blueprint('dashboard', __name__,template_folder='ironylabeller/templates')

@dashboard.route("/logout")
@roles_accepted('Admin')
def logout():
    return redirect(url_for('user.logout',next="/dashboard"))

@dashboard.route("/")
@roles_accepted('Admin')
def index():
    ''' Entrada principal'''
    return render_template("dashboard.html")

@dashboard.route("/add/user", methods=["GET", "POST"])
@roles_accepted('Admin')
def add_labeller():
    '''Agregar usuario'''
    form = NewUser()
    tasks = Task.query.all()
    roles = Role.query.all()
    form.taskid.choices=[(task.id,task.name) for task in tasks]
    form.roleids.choices=[(role.id,role.name) for role in roles]
    if form.cancel.data:
        return redirect(url_for('.index'))
    elif form.validate_on_submit():
        nuser = User(
            username=form.username.data, active=True,
            name=form.name.data,
            taskid=form.taskid.data,
            password=user_manager.hash_password(form.password.data))
        for role_id in form.roleids.data:
            role = Role.query.filter(Role.id==role_id).first()
            if role:
                nuser.roles.append(role)
        db.session.add(nuser)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template("newlabeller.html", form=form)

@dashboard.route("/edit/user/<username>", methods=["GET", "POST"])
@roles_accepted('Admin')
def edit_labeller(username):
    '''Editar usuario'''
    try:
        l=User.query.filter(User.username==username).one()
    except MultipleResultsFound, e:
        return render_template('error.html',message="Más de un usuario con el mismo nombre encontrado")
    except NoResultFound, e:
        return render_template('error.html',message="Usuario no encontrado")
    form=EditLabeller()
    tasks = Task.query.all()
    roles = Role.query.all()
    form.taskid.choices=[(task.id,task.name) for task in tasks]
    form.roleids.choices=[(role.id,role.name) for role in roles]
 
    if form.cancel.data:
        return redirect(url_for('.index'))
    if form.validate_on_submit():
        l.username=form.username.data
        l.name=form.name.data
        l.taskid=int(form.taskid.data)
        if len(form.password.data)>0:
            l.password=user_manager.hash_password(form.password.data)
        l.roles[:]=[]
        for role_id in form.roleids.data:
            role = Role.query.filter(Role.id==role_id).first()
            if role:
                l.roles.append(role)
        db.session.add(l)
        db.session.commit()
        return redirect(url_for('.index'))
    form.taskid.data=l.taskid
    form.username.data=l.username
    form.name.data=l.name
    form.roleids.data=[role.id for role in l.roles]
    return render_template("editlabeller.html", form=form,username=username)

@dashboard.route("/list/labellers")
@roles_accepted('Admin')
def list_labellers():
    '''Lista usuarions'''
    users=db.session.query(User).join(User.roles).\
                options(contains_eager(User.roles)).\
                    filter(Role.name == 'Labeller')
    return render_template("listlabellers.html", users=users)

@dashboard.route("/list/users")
@roles_accepted('Admin')
def list_users():
    '''Lista usuarions'''
    users=User.query.all()
    return render_template("listlabellers.html", users=users)

@dashboard.route("/info/user/<username>", methods=["GET", "POST"])
@roles_accepted('Admin')
def info(username):
    '''Editar usuario'''
    user=User.query.filter(User.username==username).first()
    labelled=Labelling.query.filter(Labelling.user_id==user.id and
            Labelling.task_id==user.task.id).count()
    tweets=len(user.task.tweets)
    return render_template("info.html",
            user=user,
            labelled=labelled,tweets=tweets)
 
