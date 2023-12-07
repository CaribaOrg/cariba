# /usr/bin/python3
# login form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField("Username", validators=[
                           InputRequired(), Length(min=4, max=15)], render_kw={
        'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border \
            rounded shadow appearance-none focus:outline-none focus:shadow-outline'
    })
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=8, max=80)], render_kw={
                                 'class': 'w-full px-3 py-2 mb-3 text-sm leading-tight \
                                    text-gray-700 border rounded shadow appearance-none \
                                        focus:outline-none focus:shadow-outline',
        'placeholder': '******************'})
    rememberMe = BooleanField("Remember me", render_kw={
                              'class': 'mr-2 leading-tight'})


class RegisterForm(FlaskForm):
    """Register form"""
    username = StringField("Username", validators=[
                           InputRequired(), Length(min=4, max=15)], render_kw={
        'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border \
            rounded shadow appearance-none focus:outline-none focus:shadow-outline'
    })
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid email")], render_kw={
        'class': 'w-full px-3 py-2 mb-3 text-sm leading-tight \
                                    text-gray-700 border rounded shadow appearance-none \
                                        focus:outline-none focus:shadow-outline',
        'placeholder': 'Enter your email'
    })
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=8, max=80)], render_kw={
                                 'class': 'w-full px-3 py-2 mb-3 text-sm leading-tight \
                                    text-gray-700 border rounded shadow appearance-none \
                                        focus:outline-none focus:shadow-outline',
        'placeholder': '******************'})
    confirm_password = PasswordField("Confirm password", validators=[
        InputRequired(), Length(min=8, max=80), EqualTo('password')], render_kw={
        'class': 'w-full px-3 py-2 mb-3 text-sm leading-tight \
                                    text-gray-700 border rounded shadow appearance-none \
                                        focus:outline-none focus:shadow-outline',
        'placeholder': '******************'})
