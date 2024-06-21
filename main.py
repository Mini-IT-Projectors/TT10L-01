#Test Flask

from flask import Flask, render_template,session, send_file, Response, request
import csv
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FieldList, SelectField
from wtforms.validators import DataRequired,EqualTo
import pandas as pd

# Create a Flask Instance
app = Flask(__name__, static_folder='static')
app.secret_key = 'cbjgdxgyjnges'
class Lecturer:
    def __init__(self, username,password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'Lecturer({self.username}, {self.password})'

class LecturerSubject:
    def __init__(self, username,subject):
        self.username = username
        self.subject = subject
    
    def __repr__(self):
        return f'LecturerSubject({self.username}, {self.subject})'


def save_lecturers():
    global lecturers
    lecturers = []
    with open('lecturer.csv','r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            lecturer = (Lecturer(row[0],row[1]))
            lecturers.append(lecturer)

def save_subject():
    global subjects
    subjects = []
    with open('subjects.csv','r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            subjects.append(row[0])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class GroupForm(FlaskForm):
    global lecturers
    save_lecturers()
    save_subject()
    group_name = StringField('Group Name', validators=[DataRequired()])
    group_leader = StringField('Group Leader',validators=[DataRequired()])
    subject = SelectField('Subject', choices=[
        (subject, subject) for subject in subjects
    ], validators=[DataRequired()])
    lecturer = SelectField('Lecturer', choices=[
        (lecturer.username, lecturer.username) for lecturer in lecturers
    ], validators=[DataRequired()])
    number_of_members = IntegerField('Number of Members', validators=[DataRequired()])
    member_names = FieldList(StringField(f'Member Name', validators=[DataRequired()], min_entries=1))
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

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ReviewForm(FlaskForm):
    subject = SelectField('Subject', choices=[
        ('Select Subject', 'Select Subject'),
        ('Mini IT Project', 'Mini IT Project'),
        ('Introduction To Physics', 'Introduction To Physics'),
        ('Mathematics III', 'Mathematics III'),
        ('Academic English', 'Academic English'),
        ('Critical Thinking', 'Critical Thinking'),
        ('Introduction To Digital System', 'Introduction To Digital System')
    ], validators=[DataRequired()])
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
    def __init__(self, username, group_name, subject,  member_names_you_review, review):
        self.username = username
        self.subject = subject
        self.group_name = group_name
        self.member_name_you_review = member_names_you_review
        self.review = review
        
    def __repr__(self):
        return f'Review({self.username}, {self.group_name}, {self.subject},  {self.member_name_you_review}, {self.review})'
 
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
    if not os.path.exists('lecturer.csv'):
        return False
    with open('lecturer.csv', mode='r') as file:
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
            if row['username'] == username:
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

def add_user(username, password):
    with open('users.csv', mode='a', newline='') as file:
        fieldnames = ['username', 'password']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'username': username, 'password': password})

def add_lecturer(username, password):
    with open('lecturer.csv', mode='a', newline='') as file:
        fieldnames = ['username', 'password']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'username': username,'password': password})
        
def save_groups():
    global groups
    groups = []
    with open('groups.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header row
            for row in reader:
                group = (Group(row[0], row[1], row[2], row[3], int(row[4]), row[5: ]))
                groups.append(group)

def save_reviews():
    global reviews
    reviews = []
    with open('reviews.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header row
            for row in reader:
                review = (Review(row[0], row[1], row[2], row[3], row[4]))
                reviews.append(review)
                     
@app.route('/')
def home():
    return render_template('home.html', title='Peer Review System')

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        if check_username(username)== False:
            if password == confirm_password:
                flash('Registration successful! You can now log in.', 'success')
                add_user(username, password)
                return redirect(url_for('login_user'))
            else:
                flash('Passwords do not match', 'danger')
        elif check_username(username) == True: 
            flash('Username already exists. Please choose a different username.', 'danger')
    return render_template('register_user.html', title='Register', form=form)

@app.route('/register_lecturer', methods=['GET', 'POST'])
def register_lecturer():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        if check_lecturer(username)== False:
            if password == confirm_password:
                flash('Registration successful! You can now log in.', 'success')
                add_lecturer(username, password)
                return redirect(url_for('login_lecturer'))
            else:
                flash('Passwords do not match', 'danger')
        elif check_lecturer(username) == True: 
            flash('Username already exists. Please choose a different username.', 'danger')

    return render_template('register_lecturer.html', title='Register', form=form)

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
    return render_template('login_user.html', title='Student Login', form=form)

@app.route('/user/home')
def index_user(): 
    global groups, reviews
    save_reviews()
    save_groups()
    username = session.get('username')
    for group in groups:
        if group.group_leader == username or username in group.member_names:
            return render_template("index_user.html",
                                groups = groups,
                                reviews=reviews,
                                username = username)
    return render_template("index_user.html",groups=groups,reviews=reviews,username=username)
    
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

@app.route('/user/view_<string:name>', methods = ['GET','POST'])
def view_person(name):
    global reviews
    save_reviews()
    for review in reviews:
        if review.member_name_you_review == name:
            return render_template("view_person.html", name = name,review=review)
    username = session.get('username')
    render_template("view_person.html",reviews=reviews,review =review, username=username)

@app.route('/login_lecturer', methods=['GET', 'POST'])
def login_lecturer():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if check_lecturer(username, password):
            flash('Login successful!', 'success')
            session['username'] = username
            return redirect(url_for('index_lecturer'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login_lecturer.html', title='Lecturer Login', form=form)

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
    return render_template('login_admin.html', title='Admin Login', form=form)

@app.route('/lecturer/home')
def index_lecturer():
    global groups, reviews
    sub =[]
    username = session.get('username')
    save_reviews()
    save_groups()
    groups_count = {"Mini IT Project": 0, "Academic English": 0, "Introduction To Physics": 0, 'Mathematics III' : 0, 'Critical Thinking' : 0, 'Introduction To Digital System' : 0}
    for group in groups:
        groups_count[group.subject] += 1
    with open('lecturer_subject.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            lecturer = (LecturerSubject(row[0], row[1]))
            if lecturer.username == username:
                subject = lecturer.subject
                sub.append(subject)                 
            
    return render_template("index_lecturer.html",
                            groups = groups,
                            groups_count = groups_count,
                            reviews = reviews,
                            sub = sub,
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

def write_groups_to_csv(groups):
    fieldnames = ['Group Name', 'Group Leader', 'Subject', 'Lecturer', 'Number of Members', 'Member Names']
    with open('groups.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for group in groups:
            writer.writerow({
                'Group Name': group.group_name,
                'Group Leader': group.group_leader,
                'Subject': group.subject,
                'Lecturer': group.lecturer,
                'Number of Members': group.number_of_members,
                'Member Names': ','.join(group.member_names)
            })

def find_group_by_name(group_name,subject):
    global groups
    for group in groups:
        if group.group_name == group_name and group.subject == subject:
            return group
    return None
 
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
            return redirect(url_for('create_group'))
    return render_template('admin_create.html',number_of_members=form.number_of_members.data if form.number_of_members.data else 0, form=form, group=group if group else {}) 

@app.route("/admin/groups_list")
def groups_list():
    # Assuming you have a list of Group objects called groups
    global groups

    return render_template('admin_groups_list.html', groups=groups)    

@app.route('/admin/update_group_<string:group_name>', methods=['GET', 'POST'])
def update_group(group_name,subject):
    global groups
    form = GroupForm()
    group_to_update = find_group_by_name(group_name,subject)
    if request.method == "POST":
        group_to_update.group_name = form.group_name.data
        group_to_update.group_leader = form.group_leader.data
        group_to_update.subject = form.subject.data
        group_to_update.lecturer = form.lecturer.data
        group_to_update.number_of_members = form.number_of_members.data
        group_to_update.member_names = [field.data for field in form.member_names.entries if field.data]
        
        for i, group in enumerate(groups):
            if group.group_name == group_name:
                groups[i] = group_to_update
                break

        write_groups_to_csv(groups)
        flash("Group updated successfully", "success")
        return redirect(url_for('groups_list'))
    if request.method == 'GET':
        form.group_name.data = group_to_update.group_name
        form.group_leader.data = group_to_update.group_leader
        form.subject.data = group_to_update.subject
        form.lecturer.data = group_to_update.lecturer
        form.number_of_members.data = group_to_update.number_of_members
        form.member_names.entries = [StringField('Member Name', default=name) for name in group_to_update.member_names]

    return render_template("update.html", form=form, group_to_update=group_to_update)

@app.route("/admin/delete_group_<string:group_name>_<string:subject>", methods=['GET', 'POST'])
def delete_group(group_name,subject):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv('groups.csv')

        # Filter the DataFrame to exclude the row with the specified group_name and subject
        df_filtered = df[~((df['Group Name'] == group_name) & (df['Subject'] == subject))]

        # Write the filtered DataFrame back to the CSV file
        df_filtered.to_csv('groups.csv', index=False)

        flash("Group deleted successfully")
    except Exception as e:
        flash(f"Whoops! There was a problem deleting the group: {str(e)}")
    
    return redirect(url_for('index_admin'))     
    
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

if __name__ == '__main__':
    app.run(debug=True)
