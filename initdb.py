#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Initialization of database for ironylabeller
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/iimas/unam
# ----------------------------------------------------------------------

import sys
import argparse
from ironylabeller import db, app
from flask_user import (
     UserManager,SQLAlchemyAdapter)
import json
import codecs
import random

def add_tweets_task(task_name,tweets,total):
    if not total:
        total=len(tweets)
    task=Task(name=task_name+"("+str(total)+')')
    for tweet in tweets[:total]:
        task.tweets.append(Tweet(tweetid=tweet[u'id'],
                text=tweet['text']))
    db.session.add(task)
    db.session.commit()
    for i in range(total):
        tweets.pop(0)



if __name__ == '__main__':
    p = argparse.ArgumentParser("Author identification")
    p.add_argument("TWEETS",
            help="JSON file with tweets")
    p.add_argument("--username",default="admin",
            action="store", dest="username",
            help="Username [admin]")
    p.add_argument("--password",default="password",
            action="store", dest="passwd",
            help="Password for admin [password]")
    p.add_argument("--name",default="Admin",
            action="store", dest="name",
            help="Name [admin]")
    p.add_argument("-f","--force",default=False,
            action="store_true", dest="force",
            help="Creates new database [admin]")
 
    opts = p.parse_args()
    input_file  = file(opts.TWEETS, "r")
    tweets = json.loads(input_file.read().decode("utf-8-sig"))

    random.shuffle(tweets)

    from ironylabeller.models import *
    db.create_all()


    add_tweets_task('test 1',tweets,20)
    add_tweets_task('test 2',tweets,20)
    add_tweets_task('Etiquetaciones grupo comun',tweets,1000)
    add_tweets_task('Etiquetaciones grupo uno',tweets,5500)
    add_tweets_task('Etiquetaciones grupo dos',tweets,5500)
    add_tweets_task('Etiquetaciones grupo tres',tweets,2000)
    add_tweets_task('Resto',tweets,None)


    user1 = User(username='admin', email='admin@example.com', active=True,
        password=app.user_manager.hash_password('password'))
    user1.roles.append(Role(name='Admin',label=u"Administrative role"))
    db.session.add(user1)
    role1 = Role(name="Labeller", label=u"Labeller role")
    role2 = Role(name="Superviser", label=u"Superviser role")
    db.session.add(role1)
    db.session.add(role2)
    db.session.commit()




