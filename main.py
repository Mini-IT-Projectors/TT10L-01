#Test Flask

from flask import Flask, render_template,session
import csv
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


# Create a Flask Instance
app = Flask(__name__, static_folder='static')
app.secret_key = 'cbjgdxgyjnges'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
def check_user(username, password):
    if not os.path.exists('users.csv'):
        return False
    with open('users.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False
# Create a route decorator
@app.route('/')
def home():
    return render_template('home.html', title='Peer Review System')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if check_user(username, password):
            flash('Login successful!', 'success')
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/home')
def index(): 
    first_name = "Akmal"
    stuff = "This is <strong>Bold</strong> Text"
    
    favorite_pizza = ["Pepperoni", "Cheese", "Mushroom", 41]
    username = session.get('username')
    return render_template("index.html",
                           first_name = first_name,
                           stuff=stuff,
                           favorite_pizza=favorite_pizza,
                           username=username)

# localhost:5000/user/john
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)

#create custom error page

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500