# /usr/bin/python3
# login form
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired

class MessageForm(FlaskForm):
    title = TextAreaField('Message', validators=[DataRequired(), Length(min=0, max=555)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=0, max=2555)])
    submit = SubmitField('Submit')