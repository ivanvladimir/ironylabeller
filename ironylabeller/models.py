#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Models for ironylabellers
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/iimas/unam
# ----------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask.ext.login import make_secure_token
from passlib.hash import pbkdf2_sha256
from database import Base
from datetime import datetime


class Admin(Base):
    __tablename__ = 'admin'
    id            = Column(Integer, primary_key=True)
    username      = Column(String(50), unique=True,nullable=False)
    name          = Column(String(120), nullable=False)
    _passwd       = Column(String(120), nullable=False)
    authenticated = Column(Boolean, default=False)

    def __init__(self, username=None, passwd=None, name=None):
        self.name     = name
        self.username = username
        self._passwd  = pbkdf2_sha256.encrypt(passwd, 
                rounds=200000,salt_size=16)

    def check_passwd(self, passwd):
        return pbkdf2_sha256.verify(passwd, self._passwd)
    def get_auth_token(self):
        return make_secure_token(self.username, unicode(self._passwd))
    def is_authenticated(self):
        return self.authenticated
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.username

class Labeller(Base):
    __tablename__ = 'labeller'
    id            = Column(Integer, primary_key=True)
    username      = Column(String(50), unique=True,nullable=False)
    name          = Column(String(120), nullable=False)
    _passwd       = Column(String(120), nullable=False)
    authenticated = Column(Boolean, default=False)

    def __init__(self, username=None, passwd=None, name=None):
        self.name     = name
        self.username = username
        self._passwd  = pbkdf2_sha256.encrypt(passwd, 
                rounds=200000,salt_size=16)

    def check_passwd(self, passwd):
        return pbkdf2_sha256.verify(passwd, self._passed)
    def get_auth_token(self):
        return make_secure_token(self.id, unicode(self._passwd))
    def is_authenticated(self):
        return self.authenticated
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.id)

