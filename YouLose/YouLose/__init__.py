"""
The flask application package.
"""

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yfsKnjzzpj8dZrYQ'
# configuring our database uri
app.config["SQLALCHEMY_ECHO"] = True;
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{username}:{password}@10.42.0.134/{dbname}".format(db_user, db_pass, db_name)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:tootyfruitychickenbooty@127.0.0.1/youlose"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    stocks_bought = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Stock_Bought(db.Model):
    price_bought = db.Column(db.Numeric)
    stock_bought = db.Column(db.String(5), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

# Commit tables to database
with app.app_context():
    db.create_all()
    db.session.commit()   

import YouLose.views
