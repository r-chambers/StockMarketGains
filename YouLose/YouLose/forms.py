from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from YouLose import User

class EnterStock(FlaskForm):
    stock = StringField('Stock', validators=[DataRequired(message='You must enter a stock'), Length(min=3, max=6, message='Stock must be between %(min)d and %(max) characters')])
    num_shares = StringField('Number of shares', validators=[DataRequired(message='You must enter a number') ] )
    #date_bought = DateField('Date you bought this stock', validators=[DataRequired(message='You must enter a date')])
    price = StringField('Price you paid per share', validators=[DataRequired(message='You must enter an amount') ])
    submit = SubmitField('Get profit!')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='You must enter a username')])
    password = PasswordField('Password', validators=[DataRequired(message='You must enter a password')])
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    username = StringField('Create a Username', validators=[DataRequired(message='You must enter a username')])
    password = PasswordField('Create a Password', validators=[DataRequired(message='You must enter a password')])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
