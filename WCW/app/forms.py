from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms import validators
from wtforms.validators import DataRequired

class ReaderForm(Form):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class BookForm(Form):
    title = StringField('name', validators=[DataRequired()])
    description = TextAreaField('password', validators=[DataRequired()])
