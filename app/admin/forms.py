from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length,Regexp
from flask_login import current_user
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(('Email'), validators=[DataRequired()])
    password = PasswordField(('Password'), validators=[DataRequired()])
    remember_me = BooleanField(('Remember Me'))
    submit = SubmitField(('Sign In'))


class RegistrationForm(FlaskForm):
    username = StringField(('Username'), validators=[DataRequired(), Length(min=6, max=20),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
    'Usernames must have only letters, '
    'numbers, dots or underscores')])
    email = StringField(('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(('Password'), validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password'), Length(min=8)])
    isAdmin = BooleanField(('isAdmin'))
    isFriend = BooleanField(('isFriend'))
    confirmed = BooleanField(('confirmed'))
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(('This username is already in use, please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(('This email is already in use, please use a different email address.'))

    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Image', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Save')

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    link = StringField('link', validators=[DataRequired()])
    picture = FileField('Image', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Save')

class ResumeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save')

class ChangePasswordForm(FlaskForm):
    password = PasswordField(('Password'), validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password'), Length(min=8)])
    submit = SubmitField('Change')

class HomepageForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    stack = StringField('stack', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    picture = FileField('Image', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Save')