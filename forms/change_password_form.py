#!/usr/bin/python3
''' This is a module for Changing Password Forms '''

from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        'Current Password', 
        validators=[DataRequired()]
    )
    new_password = PasswordField(
        'New Password', 
        validators=[DataRequired()]
    )
    confirm_new_password = PasswordField(
        'Confirm New Password', 
        validators=[DataRequired()]
    )