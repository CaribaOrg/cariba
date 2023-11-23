#!/usr/bin/python3
''' This is a module for Login Forms '''

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = TextField(
        'Username', 
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired()]
    )

