#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Bases for ironylabellers
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/iimas/unam
# ----------------------------------------------------------------------

from flask.ext.user import UserMixin
from ironylabeller import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

    # User email information
    email = db.Column(db.String(255), nullable=True, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    name = db.Column(db.String(100), nullable=False, server_default='')

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                backref=db.backref('users', lazy='dynamic'))
    taskid = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    task   = db.relationship("Task")


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'',
            unique=True)  
    label = db.Column(db.Unicode(255), server_default=u'')  

class UserRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Tweet(db.Model):
    __tablename__ = 'tweets'
    id        = db.Column(db.Integer(), primary_key=True)
    tweetid   = db.Column(db.String(), nullable=False, server_default='')
    text      = db.Column(db.String(180), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))

class Task(db.Model):
    __tablename__ = 'tasks'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(120), nullable=False)
    tweets        = db.relationship("Tweet")

class Labelling(db.Model):
    __tablename__ = 'labellings'
    id            = db.Column(db.Integer, primary_key=True)
    labelled      = db.Column(db.Boolean(), nullable=False)
    ironic        = db.Column(db.Boolean(), nullable=True)
    containsImage = db.Column(db.Boolean(), nullable=False)
    containsLink  = db.Column(db.Boolean(), nullable=False)
    retweet       = db.Column(db.Boolean(), nullable=False)
    doubt         = db.Column(db.Boolean(), nullable=False)
    time          = db.Column(db.Float(), nullable=False)

    # Relationships
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    tweet = db.relationship("Tweet")
    
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    task = db.relationship("Task")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User")
