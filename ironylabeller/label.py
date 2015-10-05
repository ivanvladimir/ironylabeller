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
def logout():
    return redirect(url_for('user.logout',next="/"))

@label.route("/supervirsor")
@roles_accepted('Superviser')
def supervisor():
    ''' Entrada principal'''
    doubts=Labelling.query.filter(Labelling.doubt==True).filter(Labelling.labelled==False).count()
    return render_template("supervisor.html",ndoubts=doubts,supervisor=True)

@label.route("/latest",methods=["GET", "POST"])
@roles_accepted('Superviser')
def latest():
    '''Imprime las últimas etiquetaciones'''
    labellings=Labelling.query.order_by(Labelling.id.desc()).limit(20)
    return render_template("latest.html",labellings=labellings,supervisor=True)



@label.route("/doubts",methods=["GET", "POST"])
@roles_accepted('Superviser')
def doubts():
    '''Checar dudas'''
    doubt=Labelling.query.filter(Labelling.doubt==True).filter(Labelling.labelled==False).order_by(Labelling.id).first()
    if not doubt:
        return render_template('error.html',message=u"No se encontró ningúna etiquetación con duda")
    form=Label()
    if request.method == "POST":
        if request.form['submit']=='ironic':
            ironic=True
        elif request.form['submit']=='noironic':
            ironic=False
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
        doubt.ironic=ironic
        doubt.dependsRetweet=dependsRetweet
        doubt.dependsImage=dependsImage
        doubt.dependsLink=dependsLink
        doubt.time=1
        doubt.labelled=True
        db.session.add(doubt)
        db.session.commit()
        return redirect(url_for('.doubts'))

    return render_template("label.html",
            user=current_user,tweet=doubt.tweet,form=form,supervisor=True,
            doubt=False)
  


@label.route('/',methods=["GET", "POST"])
@login_required
def index():
    ''' Entrada principal'''
    roles=[r.name for r in current_user.roles]
    supervisor=False
    if 'Admin' in roles:
        return redirect(url_for('dashboard.index'))
    if 'Superviser' in roles:
        supervisor=True
    last=Labelling.query.filter(Labelling.user_id==current_user.id).filter(
            Labelling.task_id==current_user.task.id).count()
    if not last == 0:
        if not len(current_user.task.tweets)== last:
            tweet=current_user.task.tweets[last]
        else:
            return render_template('finish.html',supervisor=supervisor)
    else:
        tweet=current_user.task.tweets[0]

    form=Label()
    if request.method == "POST":
        print(request.form)
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
        try:
            request.form['time']
            time=float(request.form['time'])/1000
        except KeyError:
            time=0.0
        
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
                dependsRetweet=dependsRetweet,
                labelled=False,
                dependsImage=dependsImage,
                dependsLink=dependsLink,
                doubt=doubt,            
                time = time)
        else:
            l.ironic=ironic
            l.dependsRetweet=dependsRetweet
            l.dependsImage=dependsImage
            l.dependsLink=dependsLink
            l.doubt=doubt
            l.time=time
        db.session.add(l)
        db.session.commit()
        return redirect(url_for('.index'))

    return render_template("label.html",
            user=current_user,tweet=tweet,form=form,supervisor=supervisor,doubt=True)


@label.route("/help")
def help():
    '''Ayuda'''
    return render_template("help.html")


