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
    SelectMultipleField,
    SubmitField, 
    IntegerField,
    SelectField,
    BooleanField,
    TextAreaField,
    validators, 
    PasswordField)


# Forms
class NewUser(Form):
    username = StringField(u'Usuario', [validators.Required()])
    name     = StringField(u'Nombre', [validators.Required()])
    password = PasswordField(u'Password', [validators.Required()])
    taskid   = SelectField(u'Tarea asignada',  coerce=int)
    roleids  = SelectMultipleField(u'Rol',  coerce=int)
    save     = SubmitField(u"Crear")
    cancel   = SubmitField(u"Cancelar")


class EditLabeller(Form):
    username = StringField(u'Usuario', [validators.Required()])
    name     = StringField(u'Nombre', [validators.Required()])
    password = PasswordField(u'Password')
    taskid   = SelectField(u'Tarea asignada',  coerce=int)
    roleids  = SelectMultipleField(u'Rol',  coerce=int)
    save     = SubmitField(u"Actualizar")
    cancel   = SubmitField(u"Cancelar")

class Label(Form):
    dependsImage   = BooleanField(u"Depende de imagen")
    dependsLink    = BooleanField(u"Contiene link")
    dependsRetweet = BooleanField(u"Viene de conversación")
    ironic         = SubmitField(u"ironic")
    noironic       = SubmitField(u"noironic")
    doubt          = SubmitField(u"doubth")

    

