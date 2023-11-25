# /usr/bin/python3
# login form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField("username", validators=[
                           InputRequired(), Length(min=4, max=15)], render_kw={
        'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border \
            rounded shadow appearance-none focus:outline-none focus:shadow-outline'
    })
    password = PasswordField("password", validators=[
                             InputRequired(), Length(min=8, max=80)], render_kw={
                                 'class': 'w-full px-3 py-2 mb-3 text-sm leading-tight \
                                    text-gray-700 border rounded shadow appearance-none \
                                        focus:outline-none focus:shadow-outline',
        'placeholder': '******************'})
    rememberMe = BooleanField("remember me", render_kw={
                              'class': 'mr-2 leading-tight'})
