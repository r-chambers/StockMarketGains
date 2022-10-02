"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, flash, url_for
from YouLose import app
from YouLose import db
# from YouLose import Book
from YouLose.forms import EnterStock
from YouLose.methods import get_present_price

def test(stock):
    teststr = get_present_price(stock)
    return teststr


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    previous_stocks = ""

    form = EnterStock()

    if request.method == "POST":
        if form.validate_on_submit():
            flash(test(form.stock.data))
            previous_stocks += "s"

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
