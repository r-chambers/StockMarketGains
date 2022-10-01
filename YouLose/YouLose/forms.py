from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

class EnterStock(FlaskForm):
    stock = StringField('Stock', validators=[DataRequired()])
    date_bought = DateField('Date you bought this stock', validators=[DataRequired()])
    submit = SubmitField('Get profit!')