from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, EmailField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange, InputRequired
import sqlalchemy as sa
from app.models import User, Post
from app import db
import re


class RegistrationForm(FlaskForm):
    """
    Registration form for creating new users.
    """
    username = StringField('Username', validators=[DataRequired()], render_kw={'style': 'width: 400px'})
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={'style': 'width: 400px'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'style': 'width: 400px'})
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={'style': 'width: 400px'})
    firstname = StringField('First Name', validators=[DataRequired()], render_kw={'style': 'width: 400px'})
    family_name = StringField('Family Name', validators=[DataRequired()], render_kw={'style': 'width: 400px'})
    country = StringField('Country', validators=[DataRequired()], render_kw={'style': 'width: 400px'})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username. This name is already taken.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email.')

    def validate_country(self, country):
        """
        Needs to be tested. This function validates if the country is in the list of countries,
        This is important for future filters of movies.
        """
        with open('app/landen.txt') as landen_file:
            landen_content = landen_file.read()  # Read the entire file content as a single string
            is_match = re.search(fr"\b{country.data.capitalize()}\b", landen_content)
        if not is_match:
            raise ValidationError('Please choose a valid country.')


class LoginForm(FlaskForm):
    """
    Login form for users who want to log in.
    """
    username = StringField('Username', validators=[DataRequired()], render_kw={'style': 'width: 400px'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'style': 'width: 400px;'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post_message = TextAreaField('Post review', render_kw={'style': 'width: device'})
    rating = IntegerField('Rating [0-10]', validators=[InputRequired(), NumberRange(min=0, max=10)],
                          render_kw={'style': 'width: 70px'})
    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    """
    Request to try and reset password
    """
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={'style': 'width: 400px'})
    submit = SubmitField('Submit')


class ResetPasswordForm(FlaskForm):
    """
    Reset password form for users who have forgotten their password.
    """
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'style': 'width: 400px'})
    confirm_password = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={'style': 'width: 400px'})
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    """
    Edit your profile information.
    """
    firstname = StringField('Firstname', validators=[DataRequired()], render_kw={'style': 'width: 400px'})
    family_name = StringField('Family_name', validators=[DataRequired()], render_kw={'style': 'width: 400px'})
    country = StringField('Country', validators=[DataRequired()], render_kw={'style': 'width: 400px'})
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_country(self, country):
        """
        Needs to be tested. This function validates if the country is in the list of countries,
        This is important for future filters of movies.
        """
        with open('app/landen.txt') as landen_file:
            landen_content = landen_file.read()  # Read the entire file content as a single string
            is_match = re.search(fr"\b{country.data.capitalize()}\b", landen_content)
        if not is_match:
            raise ValidationError('Please choose a valid country.')
