#Test Flask

from flask import Flask, render_template,session, send_file, Response, request
import csv
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FieldList, SelectField
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
            if row['lecturers'] == username:
                return True
    return False
#Read Group Name and Total Members
def check_group(subject,group_name,member_name):
    if not os.path.exists('groups.csv'):
        return False
    with open('groups.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Group Name'] == group_name and row['Subject'] == subject and member_name in row['Member Names']:
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

groups = []
@app.route('/user/home')
def index_user(): 
    username = session.get('username')
    groups = None
    with open('groups.csv', mode='r') as file:
        groups = get_all_groups_from_csv()
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row["Group Leader"] == username or username in row['Member Names']:
                return render_template("index_user.html",
                                    groups = groups,
                                    username = username)
    return render_template("index_user.html",groups=groups)
    
    
class ReviewForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    group_name = StringField('Group Name', validators=[DataRequired()])        
    member_name_you_review = StringField('Member Name', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField('Send')

if not os.path.exists('reviews.csv'):
    with open('reviews.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Group Name', 'Subject', 'Member Names You Review', 'Review'])  # header row

def add_review_to_csv(username, review):
    with open('reviews.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([username, review.group_name, review.subject, review.member_name_you_review, review.review])

class Review:
    def __init__(self, username, subject, group_name, member_names_you_review, review):
        self.username = username
        self.subject = subject
        self.group_name = group_name
        self.member_name_you_review = member_names_you_review
        self.review = review
        
    def __repr__(self):
        return f'Group({self.username}, {self.subject}, {self.group_name}, {self.member_name_you_review}, {self.review})'
    

@app.route('/user/review', methods=['GET', 'POST'])
def user_review():
    form = ReviewForm()
    review= None
    username = session.get('username')
    if form.validate_on_submit():
        subject = form.subject.data
        group_name = form.group_name.data
        member_name_you_review = form.member_name_you_review.data
        if check_group(subject,group_name,member_name_you_review):
            flash('Login successful!', 'success')
            
        review = Review(username, form.subject.data, form.group_name.data, form.member_name_you_review.data, form.review.data)
        add_review_to_csv(username,review)
        return redirect(url_for('user_review'))    
    return render_template("review_user.html",
                           username = username,
                           form=form,
                           review=review if review else {})

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
    
    groups = get_all_groups_from_csv()
    mini_it_groups = 0
    physics_groups = 0
    english_groups = 0
    with open('groups.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Subject'] == "Mini IT":
                mini_it_groups += 1
            if row['Subject'] == "Introduction To Physics":
                physics_groups += 1
            if row['Subject'] == "Academic English":
                english_groups += 1
        
    
    username = session.get('username')
    return render_template("index_admin.html",
                            groups = groups,
                            mini_it_groups = mini_it_groups,
                            physics_groups = physics_groups,
                            english_groups = english_groups,
                            username = username)
#Admin create group

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

def write_groups_to_csv(groups):
    fieldnames = ['group_name', 'group_leader', 'subject', 'lecturer', 'number_of_members', 'member_names']
    with open('groups.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for group in groups:
            writer.writerow({
                'group_name': group.group_name,
                'group_leader': group.group_leader,
                'subject': group.subject,
                'lecturer': group.lecturer,
                'number_of_members': group.number_of_members,
                'member_names': ','.join(group.member_names)
            })
            
class GroupForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired()])
    group_leader = StringField('Group Leader',validators=[DataRequired()])
    subject = SelectField('Subject', choices=[
        ('Select Subject', 'Select Subject'),
        ('Mini IT Project', 'Mini IT Project'),
        ('Introduction To Physics', 'Introduction To Physics'),
        ('Mathematics III', 'Mathematics III'),
        ('Academic English', 'Academic English'),
        ('Critical Thinking', 'Critical Thinking'),
        ('Introduction To Digital System', 'Introduction To Digital System')
    ], validators=[DataRequired()])
    lecturer = SelectField('Lecturer', choices=[
        ('Select Lecturer', 'Select Lecturer'),
        ('Suhaini Binti Nordin', 'Suhaini Binti Nordin'),
        ('Zubair Hassan Tarif', 'Zubair Hassan Tarif'),
        ('Munirah Binti Munawar Ali', 'Munirah Binti Munawar Ali'),
        ('Khairi Shazwan Bin Dollmat', 'Khairi Shazwan Bin Dollmat'),
        ('Muhammad Effendi Bin Ismail', 'Muhammad Effendi Bin Ismail'),
        ('Mohammad Shadab Khan', 'Mohammad Shadab Khan')
    ], validators=[DataRequired()])
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
        if form.lecturer.data == 'Select Lecturer' or form.subject.data == 'Select Subject':
            flash('Please select a valid lecturer or subject', 'danger')
            return redirect(url_for('create_group'))
        else:
            group = Group(form.group_name.data, form.group_leader.data, form.subject.data, form.lecturer.data, form.number_of_members.data, member_names)
            add_group_to_csv(group, member_names)
            flash('Group created successfully!')
            return redirect(url_for('groups_list'))
    return render_template('admin_create.html',number_of_members=form.number_of_members.data if form.number_of_members.data else 0, form=form, group=group if group else {}) 

@app.route("/admin/groups_list")
def groups_list():
    # Assuming you have a list of Group objects called groups
    groups = get_all_groups_from_csv()

    return render_template('admin_groups_list.html', groups=groups)    

@app.route('/admin/update_group_<string:group_name>', methods=['GET', 'POST'])
def update_group(group_name):
    form = GroupForm()
    groups = get_all_groups_from_csv()
    group_to_update = next((g for g in groups if g.group_name == group_name), None)
    
    if not group_to_update:
        flash("Group not found", "danger")
        return redirect(url_for('groups_list'))
    
    if request.method == "POST" and form.validate_on_submit():
        group_to_update['group_name'] = form.group_name.data
        group_to_update['group_leader'] = form.group_leader.data
        group_to_update['subject'] = form.subject.data
        group_to_update['lecturer'] = form.lecturer.data
        group_to_update['number_of_members'] = form.number_of_members.data
        group_to_update['member_names'] = [member_name.data for member_name in form.member_names]
        
        try:
            write_groups_to_csv(groups)
            flash("Group Updated Successfully", "success")
            return redirect(url_for('groups_list'))
        except Exception as e:
            flash(f"Error! Looks like there was a problem: {e}", "danger")
            return render_template("update.html", form=form, group_to_update=group_to_update)
    
    if request.method == "GET":
        form.group_name.data = group_to_update.group_name
        form.group_leader.data = group_to_update.group_leader
        form.subject.data = group_to_update.subject
        form.lecturer.data = group_to_update.lecturer
        form.number_of_members.data = group_to_update.number_of_members
        form.member_names.entries = [StringField('Member Name', validators=[DataRequired()], default=member) for member in group_to_update.member_names]
  
  
    return render_template("update.html", form=form, group_to_update=group_to_update) 
   
    

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