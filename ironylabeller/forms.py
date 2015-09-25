#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# forms for irony labeller
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/iimas/unam
# ----------------------------------------------------------------------

# Flask imports
from flask_wtf import Form
from wtforms import (
    StringField, 
    SelectField,
    SubmitField, 
    IntegerField,
    SelectField,
    TextAreaField,
    validators, 
    PasswordField)


# Forms
class LoginAdmin(Form):
    admin    = StringField(u'Administrador', [validators.Required()])
    passwd   = PasswordField(u'Password', [validators.Required()])
    save     = SubmitField(u"Entrar")
    cancel   = SubmitField(u"Cancelar")

class NewLabeller(Form):
    username = StringField(u'Usuario', [validators.Required()])
    name     = StringField(u'Nombre', [validators.Required()])
    passwd   = PasswordField(u'Password', [validators.Required()])
    taskid   = SelectField(u'Tarea asignada',  coerce=int)
    save     = SubmitField(u"Crear")
    cancel   = SubmitField(u"Cancelar")

