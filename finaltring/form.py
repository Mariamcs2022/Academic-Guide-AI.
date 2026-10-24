from flask_wtf import FlaskForm 
from wtforms import StringField , PasswordField ,SubmitField
from wtforms.validators import DataRequired,Length,Email, Regexp


class RegistrationForm(FlaskForm):
    fname = StringField('First name', validators=[DataRequired(), Length(min=2, max=25)])
    lname = StringField('Last name', validators=[DataRequired(), Length(min=2, max=25)])
    school = StringField('Name School', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&_\\-])[A-Za-z\\d@$!%*?&_\\-]{8,32}$")
    ])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField ('Email' , validators=[DataRequired() , Email()])
    password = PasswordField ('Password' , validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationAdmin(FlaskForm):
    fname = StringField('First name', validators=[DataRequired(), Length(min=2, max=25)])
    lname = StringField('Last name', validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&_\\-])[A-Za-z\\d@$!%*?&_\\-]{8,32}$")
    ])
    submit = SubmitField('سجل')


class LoginAdmin(FlaskForm):
    email = StringField ('Email' , validators=[DataRequired() , Email()])
    password = PasswordField ('Password' , validators=[DataRequired()])
    submit = SubmitField('الدخول')







