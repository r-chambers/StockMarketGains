"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, flash, url_for
from YouLose import app
from YouLose import db
from YouLose import User
# from YouLose import Book
from YouLose.forms import EnterStock, LoginForm, SignupForm
from YouLose.methods import get_present_price
from flask_login import current_user, logout_user, login_user

def test(stock):
    teststr = get_present_price(stock)
    return teststr


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = EnterStock()
    
    if request.method == "POST":
        if form.validate_on_submit():
            flash(test(form.stock.data))

           '''
           if current_user.is_authenticated:
                stock_price = get_present_price(form.stock.data)

                stock_bought = Stock_Bought(price_brought=stock_price, stock_bought=form.stock.data, user_id=888)
'''

            #book1 = Book(title=form.stock.data)
            #db.session.add(book1)
            #db.session.commit()

            return redirect(url_for('home'))

    """Renders the home page."""
    return render_template(
        'home.html',
        title='You Lose!',
        year=datetime.now().year,
        form = form
        )
    

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user) 
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)
    
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template("signup.html", title="Sign up", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
