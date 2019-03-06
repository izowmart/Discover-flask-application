from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=6)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(message='kindly input a valid email address'), Length(min=6, max=50)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6),
                                         EqualTo('confirm', message='Password does not match')]
                             )
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
