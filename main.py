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

#Read Student Name    
def check_user(username, password):
    if not os.path.exists('users.csv'):
        return False
    with open('users.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

def check_username(username):
    if not os.path.exists('users.csv'):
        return False
    with open('users.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['username'] == username:
                return True
    return False

#Read Admin Name
def check_admin(username, password):
    if not os.path.exists('admin.csv'):
        return False
    with open('admin.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

#Read Lecturer Name
def check_lecturer(username) :
    if not os.path.exists('lecturer.csv'):
        return False
    with open('lecturer.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['lecturer_username'] == username:
                return True
    return False

@app.route('/')
def home():
    return render_template('home.html', title='Peer Review System')

@app.route('/user_login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if check_user(username, password):
            flash('Login successful!', 'success')
            session['username'] = username
            return redirect(url_for('index_user'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login_user.html', title='Login', form=form)

@app.route('/user/home')
def index_user(): 
    first_name = "Akmal"
    stuff = "This is <strong>Bold</strong> Text"
    
    favorite_pizza = ["Pepperoni", "Cheese", "Mushroom", 41]
    username = session.get('username')
    return render_template("index_user.html",
                           first_name = first_name,
                           stuff=stuff,
                           favorite_pizza=favorite_pizza,
                           username=username)

@app.route('/admin_login', methods=['GET', 'POST'])
def login_admin():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if check_admin(username, password):
            flash('Login successful!', 'success')
            session['username'] = username
            return redirect(url_for('index_admin'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login_admin.html', title='Login', form=form)

@app.route('/admin/home')
def index_admin():
    
    groups = ["Group 1", "Group 2", "Group 3", "Group 4"]
    no_groups = len(groups)
    username = session.get('username')
    return render_template("index_admin.html",
                           groups = groups,
                           no_groups = no_groups,
                           username=username)

#Admin create group
groups = []
@app.route("/admin/create_group", methods=['GET', 'POST'])
def create_group():
    if request.method == "POST":
        group_name = request.form.get("group_name")
        group_leader = request.form.get("group_leader")
        subject = request.form.get("subject")
        lecturer = request.form.get("lecturer")
        if check_username(username) and check_lecturer(lecturer):
            groups.append({"group_name": group_name, "group_leader": group_leader, "subject": subject, "lecturer": lecturer})
    username = session.get('username')
    return render_template("admin_create.html",
                           csv_data = groups,
                           username=username)
#Number of members
@app.route('/admin/member_group', methods=['POST'])
def member_group():
    num_members = int(request.form.get('members'))
    member_names = []
    for i in range(num_members):
        member_name = request.form.get(f'member_{i+1}')
        if check_username(member_name):
            member_names.append(member_name)
    merged_member_names = ', '.join(member_names)
    return render_template('member_group.html',
                           merged_member_names=merged_member_names)
    

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