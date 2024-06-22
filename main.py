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

class Student:
    def __init__(self, username,password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'LecturerSection({self.username}, {self.password})'

def save_student():
    global students
    students = []
    with open('users.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header row
            for row in reader:
                student = (Student(row[0], row[1]))
                students.append(student)
    return students
                
class Lecturer:
    def __init__(self, username,password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'Lecturer({self.username}, {self.password})'

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
    return subjects
            
def lecturers_section():
    global lecturers_section
    lecturers_section = []
    with open('lecturer_section.csv','r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            lecturers_section.append(row[0])
    return lecturers_section
            
def tutorials_section():
    global tutorials_section
    tutorials_section = []
    with open('tutorial_section.csv','r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            tutorials_section.append(row[0])
    return tutorials_section
            
def save_lecturer_subject():
    global lecturers_subject
    lecturers_subject = []
    with open('lecturer_subject.csv','r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            lecturer_subject = (LecturerSection(row[0], row[1], row[2], row[3]))
            lecturers_subject.append(lecturer_subject)
            
class LecturerSectionForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(LecturerSectionForm, self).__init__(*args, **kwargs)
        self.subject.choices = [(subject, subject) for subject in save_subject()]

    
    lecturers_section()
    tutorials_section()
    subject = SelectField('Subject', validators=[DataRequired()])
    lecturer_section = SelectField('Lecturer Section', choices=[
        (lecturer_section, lecturer_section) for lecturer_section in lecturers_section
    ], validators=[DataRequired()])
    tutorial_section = SelectField('Tutorial Section', choices=[
        (tutorial_section, tutorial_section) for tutorial_section in tutorials_section
    ], validators=[DataRequired()])
    submit = SubmitField('Create Group')

class LecturerSection:
    def __init__(self, username,subject,lecturer_section,tutorial_section):
        self.username = username
        self.subject = subject
        self.lecturer_section = lecturer_section
        self.tutorial_section = tutorial_section
    
    def __repr__(self):
        return f'LecturerSection({self.username}, {self.subject}, {self.lecturer_section}, {self.tutorial_section})'

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class GroupForm(FlaskForm):
    global lecturers,lecturers_section,tutorials_section,subjects
    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.subject.choices = [(subject, subject) for subject in save_subject()]
        self.group_leader.choices = [(student.username, student.username) for student in save_student()]

    save_student()
    save_lecturers()
    save_subject()
    group_name = StringField('Group Name', validators=[DataRequired()])
    group_leader = SelectField('Group Leader',validators=[DataRequired()])
    subject = SelectField('Subject', validators=[DataRequired()])
    lecturer = SelectField('Lecturer', choices=[
        (lecturer.username, lecturer.username) for lecturer in lecturers
    ], validators=[DataRequired()])
    lecturer_section = SelectField('Lecturer Section', choices=[
        (lecturer_section, lecturer_section) for lecturer_section in lecturers_section
    ], validators=[DataRequired()])
    tutorial_section = SelectField('Tutorial Section', choices=[
        (tutorial_section, tutorial_section) for tutorial_section in tutorials_section
    ], validators=[DataRequired()])
    number_of_members = IntegerField('Number of Members', validators=[DataRequired()])
    member_names = FieldList(StringField(f'Member Name', validators=[DataRequired()], min_entries=1))
    submit = SubmitField('Create Group')

class Group:
    def __init__(self, group_name, group_leader, subject, lecturer, lecturer_section, tutorial_section, number_of_members, member_names):
        self.group_name = group_name
        self.group_leader = group_leader
        self.subject = subject
        self.lecturer = lecturer
        self.lecturer_section = lecturer_section
        self.tutorial_section = tutorial_section
        self.number_of_members = number_of_members
        self.member_names = member_names

    def __repr__(self):
        return f'Group({self.group_name}, {self.group_leader}, {self.subject}, {self.lecturer}, {self.lecturer_section}, {self.tutorial_section}, {self.number_of_members}, {self.member_names})'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ReviewForm(FlaskForm):
    subject = SelectField('Subject', choices=[
        (subject, subject) for subject in subjects
    ], validators=[DataRequired()])
    lecturer = SelectField('Lecturer', choices=[
        (lecturer.username, lecturer.username) for lecturer in lecturers
    ], validators=[DataRequired()])
    group_name = StringField('Group Name', validators=[DataRequired()])
    lecturer_section = SelectField('Lecturer Section', choices=[
        (lecturer_section, lecturer_section) for lecturer_section in lecturers_section
    ], validators=[DataRequired()]) 
    tutorial_section = SelectField('Tutorial Section', choices=[
        (tutorial_section, tutorial_section) for tutorial_section in tutorials_section
    ], validators=[DataRequired()])
    member_names_you_review = StringField('Member Name', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField('Send')

if not os.path.exists('reviews.csv'):
    with open('reviews.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Group Name', 'Subject','Lecturer', 'Lecturer Section', 'Tutorial Section', 'Member Names You Review', 'Review'])  # header row

def add_review_to_csv(username, review):
    with open('reviews.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([username, review.group_name, review.subject, review.lecturer, review.lecturer_section, review.tutorial_section, review.member_names_you_review, review.review])

class Review:
    def __init__(self, username, group_name, subject, lecturer, lecturer_section, tutorial_section, member_names_you_review, review):
        self.username = username
        self.subject = subject
        self.group_name = group_name
        self.lecturer = lecturer
        self.lecturer_section = lecturer_section
        self.tutorial_section = tutorial_section
        self.member_names_you_review = member_names_you_review
        self.review = review
        
    def __repr__(self):
        return f'Review({self.username},{self.group_name}, {self.subject}, {self.lecturer}, {self.lecturer_section}, {self.tutorial_section} ,  {self.member_names_you_review}, {self.review})' 

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
                group = (Group(row[0], row[1], row[2], row[3], row[4], row[5],int(row[6]), row[7: ]))
                groups.append(group)

def save_reviews():
    global reviews
    reviews = []
    with open('reviews.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header row
            for row in reader:
                review = (Review(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
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
            flash('Invalid username or paword', 'danger')
    return render_template('login_user.html', title='Student Login', form=form)

@app.route('/user/home')
def index_user(): 
    global groups, reviews, subjects
    sub = []
    save_reviews()
    save_subject()
    save_groups()
    username = session.get('username')
    for group in groups:
        if username == group.group_leader or username in group.member_names:
            return render_template("index_user.html",
                                groups = groups,
                                reviews=reviews,
                                subjects = subjects,
                                username = username)
        for subject in subjects:
            if subject in group.subject:
                one_subject = group.subject
                if one_subject not in sub:
                    sub.append(one_subject)
    return render_template("index_user.html",groups=groups,reviews=reviews,subjects = subjects, sub = sub,username=username)

@app.route('/user/review', methods=['GET', 'POST'])
def user_review():
    form = ReviewForm()
    review= None
    username = session.get('username')
    if form.validate_on_submit():
        subject = form.subject.data
        group_name = form.group_name.data
        member_names_you_review = form.member_names_you_review.data
        if check_group(subject,group_name,member_names_you_review):
            flash('Login successful!', 'success')
            
        review = Review(username, form.group_name.data, form.subject.data, form.lecturer.data, form.lecturer_section.data, form.tutorial_section.data, form.member_names_you_review.data, form.review.data)
        add_review_to_csv(username,review)
        return redirect(url_for('user_review'))    
    return render_template("review_user.html",
                           username = username,
                           form=form,
                           review=review if review else {})

@app.route('/lecturer_login', methods=['GET', 'POST'])
def login_lecturer():
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
    return render_template('login_lecturer.html', title='Lecturer Login', form=form)

@app.route('/lecturer/home')
def index_admin():
    global groups, reviews, subjects
    sub =[]
    username = session.get('username')
    save_reviews()
    save_groups()
    save_subject()
    groups = groups
    with open('lecturer_subject.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            lecturer = (LecturerSection(row[0], row[1], row[2], row[3]))
            if lecturer.username == username:
                subject = lecturer.subject
                if subject not in sub:
                    sub.append(subject)                 

    return render_template("index_lecturer.html",
                            subjects = subjects,
                            groups = groups,
                            reviews = reviews,
                            sub = sub,
                            username = username)

def add_lecturer_subject_to_csv(username, lecturer):
    with open('lecturer_subject.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([username, lecturer.subject, lecturer.lecturer_section, lecturer.tutorial_section])

def add_subject_to_csv(subject):
    with open('subjects.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([subject.subject])

@app.route("/lecturer/add_section", methods = ['POST','GET'])
def add_section():
    global subjects
    subjects = []
    with open('subjects.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            subject = (LecturerSubject(row[0]))
            subjects.append(subject)
    form = LecturerSectionForm()
    username = session.get('username')
    lecturer = None
    if form.validate_on_submit():
        subject = form.subject.data
        lecturer_section = form.lecturer_section.data
        tutorial_section = form.tutorial_section.data
        lecturer = LecturerSection(username, subject, lecturer_section, tutorial_section)
        add_lecturer_subject_to_csv(username,lecturer)
        return redirect(url_for('add_section'))    
    return render_template("add_section.html",
                           subjects = subjects,
                           username = username,
                           form=form,
                           lecturer=lecturer if lecturer else {})
    
class LecturerSubjectForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    submit = SubmitField('Add Subject')
     
class LecturerSubject:
    def __init__(self,subject):
        self.subject = subject
    def __repr__(self):
        return f'Review({self.subject})'
 
@app.route("/lecturer/add_subject", methods = ['GET','POST'])
def add_subject():
    global subjects
    subjects = []
    with open('subjects.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            subject = (LecturerSubject(row[0]))
            subjects.append(subject)
    form = LecturerSubjectForm()
    if form.validate_on_submit():
        subject = form.subject.data
        lecturer_subject = LecturerSubject(subject)
        add_subject_to_csv(lecturer_subject)
        return redirect(url_for('add_subject'))
    return render_template("add_subject.html",form=form)
    
    
#Admin create group

if not os.path.exists('groups.csv'):
    with open('groups.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Group Name', 'Group Leader', 'Subject', 'Lecturer', 'Lecturer Section', 'Tutorial Section', 'Number of Members', 'Member Names'])  # header row
        
def add_group_to_csv(group, member_names):
    with open('groups.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([group.group_name, group.group_leader, group.subject, group.lecturer, group.lecturer_section, group.tutorial_section, group.number_of_members, ', '.join(member_names)])

@app.route("/lecturer/create_group", methods=['GET','POST'])
def create_group():
    global subjects,students
    save_subject()
    save_student()
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
            group = Group(form.group_name.data, form.group_leader.data, form.subject.data, form.lecturer.data, form.lecturer_section.data,  form.tutorial_section.data, form.number_of_members.data, member_names)
            add_group_to_csv(group, member_names)
            flash('Group created successfully!')
            return redirect(url_for('create_group'))
    return render_template('admin_create.html',number_of_members=form.number_of_members.data if form.number_of_members.data else 0, form=form, group=group if group else {},students=students) 

@app.route("/lecturer/delete_group_<string:group_name>_<string:subject>", methods=['GET', 'POST'])
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
