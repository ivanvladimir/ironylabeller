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
    SubmitField, 
    IntegerField,
    SelectField,
    TextAreaField,
    validators, 
    PasswordField)


# Forms
class LoginAdmin(Form):
    admin    = StringField('Administrador', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    save     = SubmitField("Entrar")
    cancel   = SubmitField("Cancelar")

class NewLabeller(Form):
    username = StringField('Usuario', [validators.Required()])
    name     = StringField('Nombre', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    save     = SubmitField("Entrar")
    cancel   = SubmitField("Cancelar")

