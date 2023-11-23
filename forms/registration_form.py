#!/usr/bin/python3
''' This is a module for Registration Forms '''
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
    username = TextField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')]
    )
    forename = TextField(
        'forename',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    surname = TextField(
        'surname',
        validators=[DataRequired(), Length(min=3, max=25)]
    )