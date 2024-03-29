# Aqui vai ficar os formularios de login e de posts

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms.widgets import TextArea

from instagram.models import User


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    btn = SubmitField('Login')


class FormCreateNewAccount(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    checkPassword = PasswordField('Check Password', validators=[DataRequired(), Length(6, 20), EqualTo('password')])
    btn = SubmitField('Create Account')

    def validate_email(self, email):
        email_of_user = User.query.filter_by(email=email.data).first()
        if email_of_user:
            return ValidationError('~ email already exists ~')


class FormCreateNewPost(FlaskForm):
    text = StringField('Post Text', widget=TextArea(), validators=[DataRequired()])
    photo = FileField('Photo', validators=[DataRequired()])
    btn = SubmitField('Publish')

class SocialForm(FlaskForm):
    block_button = SubmitField('Bloquear')
