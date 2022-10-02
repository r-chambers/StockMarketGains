"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, flash, url_for
from YouLose import app
from YouLose import db
from YouLose import User, Stock_Bought, Stock_Prices
# from YouLose import Book
from YouLose.forms import EnterStock, LoginForm, SignupForm
from YouLose.methods import get_present_price
from flask_login import current_user, logout_user, login_user

def test(stock):
    teststr = float(get_present_price(stock))
    print(teststr)
    print(type(teststr))
    return teststr

def profit(num_shares, stock_current_price, price_bought_at):
    return 30

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = EnterStock()
    stock_count = 0 
    
    if current_user.is_authenticated:
        stocks = Stock_Bought.query.join(Stock_Prices, Stock_Bought.stock_bought == Stock_Prices.stock_name).add_columns(Stock_Prices.stock_name, Stock_Prices.stock_current_price, Stock_Bought.stock_bought, Stock_Bought.profit, Stock_Bought.num_shares_bought, Stock_Bought.price_bought, Stock_Bought.user_id).filter(Stock_Bought.user_id == current_user.id)
        stock_count = stocks.count()

        # hold data from query
        '''
        stock_dicts = []
        for stock_row in stocks:
            stock_dicts += [
                {'stock_name': stock_row.stock_name, 'stock_current_price': stock_row.stock_current_price, 'stock_price_brought': stock_row.stock_price_bought}
                ]
            print (stock_row.stock_name)
            print("**********")'''

    if request.method == "POST":
        if form.validate_on_submit():
            if current_user.is_authenticated:
                new_stock_price = test(form.stock.data)

                check_stock_price = Stock_Prices.query.filter_by(stock_name=form.stock.data).first()
                # if the stock we're getting the price for isn't in the stock_price database, then add it
                if check_stock_price is None:
                    stock_price_add = Stock_Prices(stock_name=form.stock.data, stock_current_price=new_stock_price)
                    db.session.add(stock_price_add)
                # if it's already in the database, then update current stock price
                else:
                    check_stock_price.stock_current_price = new_stock_price
                # commit changes to stock_prices database
                db.session.commit()
                # Add user's stock to database
                
                # Check to see if user has already added a stock
                check_sock = Stock_Bought.query.filter_by(stock_bought=form.stock.data, user_id=current_user.id).first()
                if check_sock is not None:
                    flash("You've already added this stock")
                else:
                    # calculate profit
                    stock_profit = profit(form.num_shares.data, new_stock_price, form.price.data)
                    # add the stock bought by the user to the database
                    stock_bought = Stock_Bought(price_bought=form.price.data, profit = stock_profit, num_shares_bought = form.num_shares.data, stock_bought=form.stock.data.upper(), user_id=current_user.id)
                    db.session.add(stock_bought)
                    db.session.commit()

            return redirect(url_for('home'))
            #book1 = Book(title=form.stock.data)
            #db.session.add(book1)
            #db.session.commit()

    return render_template('home.html', title='You Lose!', year=datetime.now().year, form = form, stocks=stocks, stock_count=stock_count)

#book1 = Book(title=form.stock.data)
#db.session.add(book1)
#db.session.commit()

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
    return redirect(url_for('home'))


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
