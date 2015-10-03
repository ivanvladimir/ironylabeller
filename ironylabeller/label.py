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
from flask_user import (
    login_required,
    current_user,
    roles_accepted)
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from ironylabeller import user_manager, db

# Local imports
from forms import NewUser, EditLabeller, Label
from models import User, Task, Labelling

# Registering Blueprint
label = Blueprint('label', __name__,template_folder='ironylabeller/templates')

@label.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))

@label.route('/',methods=["GET", "POST"])
@login_required
def index():
    ''' Entrada principal'''
    form=Label()
    if request.method == "POST":
        l=Labelling(
            task_id=current_user.task.id,
            user_id=current_user.id,
            ironic=True,
            labelled=True,
            containsImage=False,
            doubt=False,            
            time = 1   
                )
        db.session.add(l)
        db.session.commit()
        return redirect(url_for('.index'))

    last=Labelling.query.filter(Labelling.user_id==current_user.id and
            Labelling.task_id==current_user.task.id).count()
    if not last == 0:
        if not len(current_user.task.tweets)== last:
            tweet=current_user.task.tweets[last]
        else:
            return render_template('error.html',message="Mucha gracias, todos los tweets de esta tarea etiquetados!")
    else:
        tweet=current_user.task.tweets[0]

    return render_template("label.html",user=current_user,tweet=tweet)
