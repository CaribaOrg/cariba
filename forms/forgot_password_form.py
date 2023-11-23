#!/usr/bin/python3
''' This is a module for Forgotten Passowrd Forms'''
from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired, Length, Email


class ForgotPassowrdForm(FlaskForm):
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
   