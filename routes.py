from flask import Flask, render_template, request, redirect, url_for, flash

from app import app
from models import db, User, Subjects, Chapters, Quizzes, Questions

from flask_login import login_user, logout_user, login_required, current_user

def toPythonDate(date):
    import datetime

    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[-2::])

    return datetime.date(year, month, day)

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        fullname = request.form.get('full-name')
        qualification = request.form.get('qualification')
        dob = toPythonDate(request.form.get('dob'))
        if len(username) < 4:
            flash('Username must be at least 4 characters long.', category='error')
        elif username == 'admin':
            flash('Username cannot be "admin".', category='error')
        elif len(password) < 4:
            flash('Password must be at least 4 characters long.', category='error')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists, try another one.', category='error')
        else:
            user = User(username=username, password=password, fullname=fullname, qualification=qualification, dob=dob)
            db.session.add(user)
            db.session.commit()
            flash('User created! Logged in successfully.', category='success')
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Username does not exist.', category='error')
            return redirect(url_for('login'))
        elif not user.check_password(password):
            flash('Incorrect password.', category='error')
            return redirect(url_for('login'))
        else:
            flash('Logged in successfully.', category='success')
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', category='success')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        if 'sub-name' in request.form:
            subjectname = request.form.get('sub-name')
            subjectdesc = request.form.get('sub-description')
            if len(subjectname) < 1:
                flash('Subject name can\'t be empty.', category='error')
                return redirect(url_for('dashboard'))
            if Subjects.query.filter_by(subjectname=subjectname).first():
                flash('Subject already exists.', category='error')
                return redirect(url_for('dashboard'))
            subject = Subjects(subjectname=subjectname, subjectdesc=subjectdesc)
            db.session.add(subject)
            db.session.commit()
            flash('Subject added successfully.', category='success')
            return render_template('dashboard.html', user = current_user, subjects = Subjects.query.all())
        if 'subject' in request.form:
            subject = request.form.get('subject')
            print(subject)
            return render_template('dashboard.html', user = current_user, subjects = Subjects.query.all(), subject = subject)

    return render_template('dashboard.html', user = current_user, subjects = Subjects.query.all())

@app.route('/admin-quiz')
@login_required
def admin_quiz():
    return 'Admin-quiz'

@app.route('/admin-summary')
@login_required
def admin_summary():
    return 'Admin-summary'

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        oldPassword = request.form.get('old-password')
        newPassword = request.form.get('new-password')
        if User.query.filter_by(username=username).first() and username != current_user.username:
            flash('Username already exists, try another one.', category='error')
        elif len(username) < 4:
            flash('Username must be at least 4 characters long.', category='error')
            redirect(url_for('profile'))
        elif len(newPassword) < 4:
            flash('Password must be at least 4 characters long.', category='error')
            redirect(url_for('profile'))
        elif not current_user.check_password(oldPassword):
            flash('Incorrect old password.', category='error')
            redirect(url_for('profile'))
        elif current_user.check_password(newPassword):
            flash('New password can\'t be same as old password.', category='error')
            redirect(url_for('profile'))
        else:
            current_user.username = username
            current_user.fullname = fullname
            current_user.password = newPassword
            db.session.commit()
            flash('Profile updated successfully.', category='success')
            redirect(url_for('profile'))
    return render_template('profile.html', user = current_user)
