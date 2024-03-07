from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
import sqlalchemy as sa
from app.models import User, Address
from app import db
import re


class RegistrationForm(FlaskForm):
    """
    Registration form for creating new users.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    firstname = StringField('First Name', validators=[DataRequired()])
    family_name = StringField('Family Name', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username. This name is already taken.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email.')

    @staticmethod
    def validate_country(self, country):
        """
        Needs to be tested. This function validates if the country is in the list of countries,
        This is important for future filters of movies.
        """
        with open('landen.txt') as landen_file:
            landen_content = landen_file.read()
            is_match = re.search(r"\b{}\b".format(eenland), landen_content)
        if is_match:
            user = db.session.scalar(sa.select(Address).where(Address.country == country.data))
            if user is not None:
                raise ValidationError('Please choose a valid country.')


class LoginForm(FlaskForm):
    """
    Login form for users who want to login.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ResetpasswordRequestForm(FlaskForm):
    """
    Request to try and reset password
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


class ResetPasswordForm(FlaskForm):
    """
    Reset password form for users who have forgotten their password.
    """
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    """
    Edit your profile information.
    """
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postalcode = StringField('Postal Code', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_number = StringField('House Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')
