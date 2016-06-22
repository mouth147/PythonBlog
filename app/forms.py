from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from flask_wtf.html5 import EmailField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired

class loginform(Form):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class CreateEntry(Form):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Content')
    published = BooleanField('Published')

class PhotoForm(Form):
    photo = FileField('Your photo', validators=[DataRequired()])

