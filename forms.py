from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, url
from wtforms.fields.html5 import EmailField, URLField


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=35)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=3, max=35)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    email = EmailField('Email Address',
                       validators=[DataRequired(), Length(min=6, max=100)])
    personal_pronouns = StringField('Personal Pronouns',
                                    validators=[DataRequired(),
                                                Length(min=2, max=20)])
    occupation = StringField('Occupation',
                             validators=[DataRequired(),
                                         Length(min=6, max=35)])
    tech_stack = StringField('Tech Stack', validators=[DataRequired(),
                                                       Length(min=6, max=150)])
    about_me = TextAreaField('About Me', validators=[Length(min=6, max=1000)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddCodeForm(FlaskForm):
    post_title = StringField('Add Title',
                             validators=[DataRequired(), Length(
                                 min=3, max=40)])
    post_input = TextAreaField('Add Post',
                             validators=[DataRequired(), Length(
                                 min=3, max=3000)])
    code_pen = StringField('Code Pen URL')
    
    submit = SubmitField('Add Post')


class AddReviewForm(FlaskForm):
    post_title = StringField('Add Title',
                             validators=[DataRequired(), Length(
                                 min=3, max=40)])
    post_input = TextAreaField('Add Post',
                             validators=[DataRequired(), Length(
                                 min=3, max=3000)])
    code_pen = StringField('Code Pen URL')
    github = StringField('Repo URl')
    deployed = StringField('Deployed Site')
    
    submit = SubmitField('Add Post')


class AddGeneralForm(FlaskForm):
    post_title = StringField('Add Title',
                             validators=[DataRequired(), Length(
                                 min=3, max=40)])
    post_input = TextAreaField('Add Post',
                             validators=[DataRequired(), Length(
                                 min=3, max=3000)])  
    github = StringField('Repo URl')
    deployed = StringField('Deployed Site')
    
    submit = SubmitField('Add Post')    

class UpdateProfileForm(FlaskForm):
    email = EmailField('Email Address',
                       validators=[DataRequired(), Length(min=6, max=35)])
    personal_pronouns = StringField('Personal Pronouns',
                                    validators=[DataRequired(),
                                                Length(min=2, max=20)])
    occupation = StringField('Occupation',
                             validators=[DataRequired(),
                                         Length(min=6, max=35)])
    tech_stack = StringField('Tech Stack', validators=[DataRequired(),
                                                       Length(min=6, max=35)])
    about_me = TextAreaField('About Me', validators=[Length(min=6, max=1000)])
    submit = SubmitField('Update')


class AddCommentForm(FlaskForm):
    comment_input = TextAreaField('Add Comment',
                             validators=[DataRequired(), Length(
                                 min=3, max=3000)])  
    submit = SubmitField('Update')