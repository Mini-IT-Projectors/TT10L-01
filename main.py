#Test Flask

from flask import Flask, render_template,session, send_file, Response, request
import csv
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FieldList
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
#Read Group Name and Total Members
def check_group(group_name,num_members):
    if not os.path.exists('groups.csv'):
        return False
    with open('groups.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['group_name'] == group_name and row['num_member'] == num_members:
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
                           username = username)

#Admin create group
groups = []

if not os.path.exists('groups.csv'):
    with open('groups.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Group Name', 'Group Leader', 'Subject', 'Lecturer', 'Number of Members', 'Member Names'])  # header row
        
def add_group_to_csv(group, member_names):
    with open('groups.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([group.group_name, group.group_leader, group.subject, group.lecturer, group.number_of_members, ', '.join(member_names)])

def get_all_groups_from_csv():
    with open('groups.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        for row in reader:
            group = (Group(row[0], row[1], row[2], row[3], row[4], row[5: ]))
            groups.append(group)
    return groups

class GroupForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired()])
    group_leader = StringField('Group Leader',validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    lecturer = StringField('Lecturer', validators=[DataRequired()])
    number_of_members = IntegerField('Number of Members', validators=[DataRequired()])
    member_names = FieldList(StringField(f'Member Name', validators=[DataRequired()]))
    submit = SubmitField('Create Group')


class Group:
    def __init__(self, group_name, group_leader, subject, lecturer, number_of_members, member_names):
        self.group_name = group_name
        self.group_leader = group_leader
        self.subject = subject
        self.lecturer = lecturer
        self.number_of_members = number_of_members
        self.member_names = member_names

    def __repr__(self):
        return f'Group({self.group_name}, {self.group_leader}, {self.subject}, {self.lecturer}, {self.number_of_members},{self.member_names})'
    
@app.route("/admin/create_group", methods=['GET','POST'])
def create_group():
    form = GroupForm()
    group = None
    if form.validate_on_submit():
        member_names = []
        for i in range(form.number_of_members.data):
            member_name = request.form[f'member_name_{i + 1}']
            member_names.append(member_name)
        group = Group(form.group_name.data, form.group_leader.data, form.subject.data, form.lecturer.data, form.number_of_members.data, member_names)
        add_group_to_csv(group, member_names)
        # Save the group data to a CSV file or database
        flash('Group created successfully!')
        return redirect(url_for('groups_list'))
    return render_template('admin_create.html',number_of_members=form.number_of_members.data if form.number_of_members.data else 0, form=form, group=group if group else {}) 

@app.route("/admin/groups_list")
def groups_list():
    # Assuming you have a list of Group objects called groups
    groups = get_all_groups_from_csv()

    return render_template('admin_groups_list.html', groups=groups)    

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = UserForm()
    csv_file = 'groups.csv'

    if request.method == "POST":
        name_to_update = {}
        with open(csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == current_user.id:
                    name_to_update = row
                    break

        if name_to_update:
            name_to_update['name'] = request.form['name']
            name_to_update['email'] = request.form['email']
            name_to_update['favorite_color'] = request.form['favorite_color']
            name_to_update['username'] = request.form['username']
            name_to_update['about_author'] = request.form['about_author']

            # Check for profile pic
            if request.files['profile_pic']:
                pic_filename = secure_filename(request.files['profile_pic'].filename)
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                request.files['profile_pic'].save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                name_to_update['profile_pic'] = pic_name

            with open(csv_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=name_to_update.keys())
                writer.writeheader()
                writer.writerow(name_to_update)

            flash("User Updated Successfully!")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
        else:
            flash("Error!  Looks like there was a problem...try again!")
            return render_template("dashboard.html", form=form, name_to_update={})
    else:
        with open(csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == current_user.id:
                    return render_template("dashboard.html", form=form, name_to_update=row)

    return render_template('dashboard.html')


@app.route("/admin/dashboard")
def admin_dashboard():
    csv_file = "groups.csv"
    with open(csv_file, "r", newline="") as file:
        reader = csv.DictReader(file)
        groups = [row for row in reader]
    return render_template("admin_dashboard.html", csv_data=groups)

@app.route("/admin/success")
def success():
    return render_template('success.html')

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