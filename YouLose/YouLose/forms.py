from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DateField

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