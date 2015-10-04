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
    if 'Admin' in [r.name for r in current_user.roles]:
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

    form=Label()
    if request.method == "POST":
        if request.form['submit']=='ironic':
            ironic=True
            doubt=False
        elif request.form['submit']=='noironic':
            ironic=False
            doubt=False
        else:
            ironic=None
            doubt=True
        try:
            request.form['dependsImage']
            dependsImage=True
        except KeyError:
            dependsImage=False
        try:
            request.form['dependsLink']
            dependsLink=True
        except KeyError:
            dependsLink=False
        try:
            request.form['dependsRetweet']
            dependsRetweet=True
        except KeyError:
            dependsRetweet=False
        l=Labelling.query.filter(
                Labelling.tweet_id==tweet.id).filter(
                    Labelling.user_id==current_user.id and
                    Labelling.task_id==current_user.task.id
            ).first()
        if  not l: 
            l=Labelling(
                task_id=current_user.task.id,
                user_id=current_user.id,
                tweet_id=tweet.id,
                ironic=ironic,
                dapandsRetweet=dapendsRetweet,
                labelled=True,
                dependsImage=dependsImage,
                depdndsLink=dependsLink,
                doubt=doubt,            
                time = 1)
        else:
            l.ironic=ironic
            l.dependsRetweet=dependsRetweet
            l.dependsImage=dependsImage
            l.dependsLink=dependsLink
            l.doubt=doubt
            l.time=1
        db.session.add(l)
        db.session.commit()
        return redirect(url_for('.index'))

    return render_template("label.html",user=current_user,tweet=tweet,form=form)
