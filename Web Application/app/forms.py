from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms import validators

class CreateForm(Form):
    title = TextField('Title', [validators.required(), validators.length(max=50)])
    description = PasswordField('Description', [validators.optional(), validators.length(max=200)])
