"""
The flask application package.
"""

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yfsKnjzzpj8dZrYQ'
# configuring our database uri
app.config["SQLALCHEMY_ECHO"] = True;
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{username}:{password}@10.42.0.134/{dbname}".format(db_user, db_pass, db_name)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:CookieBookie345@127.0.0.1/youlose"

db = SQLAlchemy(app)
login = LoginManager(app)
db.configure_mappers()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #total_profit = db.Column(db.Float)
    stocks_bought = db.relationship('Stock_Bought', backref='userid', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<User {}>'.format(self.username)

class Stock_Bought(db.Model):
    price_bought = db.Column(db.Float)
    profit = db.Column(db.Float)
    num_shares_bought = db.Column(db.Integer)
    stock_bought = db.Column(db.String(5), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    #stock_price = db.relationship("Stock_Prices", backref="stock_price", lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.stock_bought)


class Stock_Prices(db.Model):
    stock_name = db.Column(db.String(5), primary_key=True)
    stock_current_price = db.Column(db.Numeric())

    def __repr__(self):
        return '<Stock name {}>'.format(self.stock_name)

# Commit tables to database
with app.app_context():
    db.create_all()
    db.session.commit()   

import YouLose.views
