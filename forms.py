from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
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
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddPostForm(FlaskForm):
    post_input = StringField('Add Post',
                             validators=[DataRequired(), Length(
                                 min=3, max=3000)])
    post_type = RadioField('Post Type', choices=[('peer', 'Peer Review'), (
        'code', 'Code Snippet'), ('general', 'General')],
                            validators=[DataRequired()])                        

    submit = SubmitField('Add Post')
