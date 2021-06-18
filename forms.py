from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=3, max=15)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    email = EmailField('Email Address',
                       validators=[DataRequired(), Length(min=6, max=35)])
    personal_pronouns = StringField('Personal Pronouns',
                                    validators=[DataRequired(),
                                                Length(min=2, max=6)])
    occupation = StringField('Occupation',
                             validators=[DataRequired(),
                                         Length(min=6, max=35)])
    tech_stack = StringField('Tech Stack', validators=[DataRequired(),
                                                       Length(min=6, max=35)])
    about_me = TextAreaField('About Me', validators=[Length(min=6, max=1000)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddPost(FlaskForm):
    post_input = StringField('Add Post',
                             validators=[DataRequired(), Length(
                                 min=3, max=3000)])

    submit = SubmitField('Add Post')
