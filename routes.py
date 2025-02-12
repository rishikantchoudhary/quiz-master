from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from app import app
from models import db, User, Subjects, Chapters, Quizzes, Questions, Scores

from flask_login import login_user, logout_user, login_required, current_user

import datetime
import json

def toPythonDate(date):
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
            if user.is_admin == True:
                return redirect(url_for('admin_dashboard'))
            else:
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
            if user.is_admin == True:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', category='success')
    return redirect(url_for('login'))

@app.route('/admin-dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
        if request.method == 'POST':
            if 'sub-name' in request.form:
                subjectname = request.form.get('sub-name')
                subjectdesc = request.form.get('sub-description')
                if len(subjectname) < 1 or len(subjectdesc) < 1:
                    flash('Subject fields can\'t be empty.', category='error')
                    return redirect(url_for('admin_dashboard'))
                if len(subjectdesc) > 512:
                    flash('Subject description can\'t be more than 512 characters.', category='error')
                    return redirect(url_for('admin_dashboard'))
                if Subjects.query.filter_by(subjectname=subjectname).first():
                    flash('Subject already exists.', category='error')
                    return redirect(url_for('admin_dashboard'))
                subject = Subjects(subjectname=subjectname, subjectdesc=subjectdesc)
                db.session.add(subject)
                db.session.commit()
                flash('Subject added successfully.', category='success')
                return redirect(url_for('admin_dashboard'))
            if 'subject' in request.form:
                subject = request.form.get('subject')
                return render_template('admin-dashboard.html', user = current_user, subjects = Subjects.query.filter_by(subjectname=subject).all(),  chapters = Chapters.query.all())
        return render_template('admin-dashboard.html', user = current_user, subjects = Subjects.query.all(), chapters = Chapters.query.all())     

@app.route('/delete-sub', methods=['POST'])
@login_required
def delete_subject():
    sub = json.loads(request.data)
    sub_id = sub['sub_id']
    sub = Subjects.query.get(sub_id)
    if sub:
        chapters = Chapters.query.filter_by(subjectid=sub_id).all()
        for chap in chapters:
            db.session.delete(chap)
        quizzes = Quizzes.query.filter_by(subjectid=sub_id).all()
        for quiz in quizzes:
            questions = Questions.query.filter_by(quizid=quiz.quizid).all()
            for ques in questions:
                db.session.delete(ques)
            db.session.delete(quiz)
        db.session.delete(sub)
        db.session.commit()
        flash('Subject deleted successfully.', category='success')
    return jsonify({})

@app.route('/delete-chap', methods=['POST'])
@login_required
def delete_chapter():
    chap = json.loads(request.data)
    chap_id = chap['chap_id']
    chap = Chapters.query.get(chap_id)
    if chap:
        questions = Questions.query.filter_by(chapterid=chap_id).all()
        for ques in questions:
            db.session.delete(ques)
        db.session.delete(chap)
        db.session.commit()
        flash('Chapter deleted successfully.', category='success')
    return jsonify({})

@app.route('/add-chapter/<int:sub_id>', methods=['GET', 'POST'])
@login_required
def add_chap(sub_id):
    if request.method == 'POST':
        subjectid = request.form.get('subject-id')
        chaptername = request.form.get('chap-name')
        chapterdesc = request.form.get('chap-description')
        if len(chaptername) < 1 or len(chapterdesc) < 1:
            flash('Chapter fields can\'t be empty.', category='error')
            return redirect(url_for('add_chap', sub_id=sub_id))
        if len(chapterdesc) > 512:
            flash('Chapter description can\'t be more than 512 characters.', category='error')
            return redirect(url_for('add_chap', sub_id=sub_id))
        if Chapters.query.filter_by(chaptername=chaptername).first():
            flash('Chapter already exists.', category='error')
            return redirect(url_for('add_chap', sub_id=sub_id))
        chapter = Chapters(subjectid=subjectid, chaptername=chaptername, chapterdesc=chapterdesc)
        db.session.add(chapter)
        db.session.commit()
        flash('Chapter added successfully.', category='success')
        return redirect(url_for('admin_dashboard'))
    subjectId = Subjects.query.get(sub_id).subjectid
    return render_template('add-chapter.html', user = current_user, subjectid = subjectId)

@app.route('/admin-quiz', methods=['GET', 'POST'])
@login_required
def admin_quiz():
    if request.method == 'POST':
        if 'subject' in request.form:
            subject = request.form.get('subject')
            subject = Subjects.query.filter_by(subjectname=subject).first().subjectid
            return render_template('quizzes.html', user = current_user, subjects = Subjects.query.all(), quizzes = Quizzes.query.filter_by(subjectid=subject).all())
        if 'quiz-name' in request.form:
            quizname = request.form.get('quiz-name')
            duration = int(request.form.get('quiz-duration'))
            subjectName = request.form.get('select-subject')
            subjectid = Subjects.query.filter_by(subjectname=subjectName).first().subjectid
            quizdate = datetime.date.today()
            if not 1 <= duration <= 240:
                flash('Quiz duration must be between 10 and 240 minutes.', category='error')
                return redirect(url_for('admin_quiz'))
            if len(quizname) < 1:
                flash('Quiz name can\'t be empty.', category='error')
                return redirect(url_for('admin_quiz'))
            if Quizzes.query.filter_by(quizname=quizname).first():
                flash('Quiz name already exists.', category='error')
                return redirect(url_for('admin_quiz'))
            quiz = Quizzes(quizname=quizname, subjectid=subjectid, duration=duration, quizdate=quizdate)
            db.session.add(quiz)
            db.session.commit()
            flash('Quiz added successfully.', category='success')
            return redirect(url_for('admin_quiz'))
    return render_template('quizzes.html', user = current_user, subjects = Subjects.query.all(), quizzes = Quizzes.query.all())

@app.route('/view-quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def view_quiz(quiz_id):
    if request.method == 'POST':
        quizid = quiz_id
        chapterid = request.form.get('select-chapter')
        title = request.form.get('question-title')
        statement = request.form.get('question-statement')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        ans = request.form.get('correct-option')
        if len(title) < 1 or len(statement) < 1 or len(option1) < 1 or len(option2) < 1 or len(option3) < 1 or len(option4) < 1:
            flash('Question fields can\'t be empty.', category='error')
            return redirect(url_for('view_quiz', quiz_id=quiz_id))
        if len(title) > 80  or len(option1) > 80 or len(option2) > 80 or len(option3) > 80 or len(option4) > 80:
            flash('Question title and options can\'t be more than 80 characters.', category='error')
            return redirect(url_for('view_quiz', quiz_id=quiz_id))
        if len(statement) > 512:
            flash('Question statement can\'t be more than 512 characters.', category='error')
            return redirect(url_for('view_quiz', quiz_id=quiz_id))
        question = Questions(quizid=quizid, chapterid=chapterid , title=title, statement=statement, option1=option1, option2=option2, option3=option3, option4=option4, ans=ans)
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully.', category='success')
        return redirect(url_for('view_quiz', quiz_id=quiz_id))
    return render_template('view-quiz.html', user = current_user, quiz = Quizzes.query.get(quiz_id), questions = Questions.query.filter_by(quizid=quiz_id).all(), chapters = Chapters.query.filter_by(subjectid=Quizzes.query.get(quiz_id).subjectid).all())


@app.route('/view-question/<int:que_id>')
@login_required
def view_question(que_id):
    return render_template('view-question.html', user = current_user, question = Questions.query.get(que_id), chapter = Chapters.query.get(Questions.query.get(que_id).chapterid).chaptername)

@app.route('/delete-question', methods=['POST'])
@login_required
def delete_question():
    ques = json.loads(request.data)
    que_id = ques['que_id']
    que = Questions.query.get(que_id)
    if que:
        db.session.delete(que)
        db.session.commit()
        flash('Question deleted successfully.', category='success')
    return jsonify({})

@app.route('/edit-quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(quiz_id):
    if request.method == 'POST':
        quizname = request.form.get('quiz-name')
        duration = int(request.form.get('quiz-duration'))
        subjectName = request.form.get('select-subject')
        if not 1 <= duration <= 240:
                flash('Quiz duration must be between 10 and 240 minutes.', category='error')
                return redirect(url_for('edit_quiz', quiz_id=quiz_id))
        if len(quizname) < 1:
            flash('Quiz name can\'t be empty.', category='error')
            return redirect(url_for('edit_quiz', quiz_id=quiz_id))
        if Quizzes.query.filter_by(quizname=quizname).first() and Quizzes.query.filter_by(quizname=quizname).first().quizid != quiz_id:
            flash('Quiz name already exists.', category='error')
            return redirect(url_for('edit_quiz', quiz_id=quiz_id))
        quiz = Quizzes.query.get(quiz_id)
        quiz.quizname = quizname
        quiz.duration = duration
        quiz.subjectid = Subjects.query.filter_by(subjectname=subjectName).first().subjectid
        db.session.commit()
        flash('Quiz updated successfully.', category='success')
        return redirect(url_for('admin_quiz'))
    return render_template('edit-quiz.html', user = current_user, quiz = Quizzes.query.get(quiz_id), subjects = Subjects.query.all())

@app.route('/delete-quiz', methods=['POST'])
@login_required
def delete_quiz():
    quiz = json.loads(request.data)
    quiz_id = quiz['quiz_id']
    quiz = Quizzes.query.get(quiz_id)
    if quiz:
        questions = Questions.query.filter_by(quizid=quiz_id).all()
        for ques in questions:
            db.session.delete(ques)
        db.session.delete(quiz)
        db.session.commit()
        flash('Quiz deleted successfully.', category='success')
    return jsonify({})

@app.route('/admin-summary')
@login_required
def admin_summary():
    return render_template('admin-summary.html', user = current_user)

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


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        subject = request.form.get('subject')
        return render_template('dashboard.html', user = current_user, subjects = Subjects.query.all(), quizzes = Quizzes.query.filter_by(subjectid=Subjects.query.filter_by(subjectname=subject).first().subjectid).all())
    return render_template('dashboard.html', user = current_user, subjects = Subjects.query.all(), quizzes = Quizzes.query.all())

@app.route('/show-quiz/<int:quiz_id>')
@login_required
def show_quiz(quiz_id):
    return render_template('show-quiz.html', user = current_user, quiz = Quizzes.query.get(quiz_id),subject = Subjects.query.get(Quizzes.query.get(quiz_id).subjectid))

@app.route('/attempt-quiz/<int:quiz_id>')
@login_required
def attempt_quiz(quiz_id):
    return render_template('attempt-quiz.html', user = current_user, quiz = Quizzes.query.get(quiz_id), questions = Questions.query.filter_by(quizid=quiz_id).all())

@app.route('/submit-quiz', methods=['POST'])
@login_required
def submit_quiz():
    response = json.loads(request.data)
    userid = response['userid']
    quizid = response['quizid']
    quizname = Quizzes.query.get(quizid).quizname
    subject = Subjects.query.get(Quizzes.query.get(quizid).subjectid).subjectname
    duration = Quizzes.query.get(quizid).duration
    selectedAnswers = response['selectedAnswers']
    attemptdate = datetime.date.today()
    correctanswers = 0
    totalquestions = len(selectedAnswers)

    for i in selectedAnswers:
        answer = Questions.query.get(i).ans
        if answer == int(selectedAnswers[i]):
            correctanswers += 1

    score = Scores(userid=userid, quizid=quizid, quizname=quizname, subject=subject, duration=duration, attemptdate=attemptdate, correctanswers=correctanswers, totalquestions=totalquestions)
    db.session.add(score)
    db.session.commit()
    flash('Quiz submitted successfully.', category='success')
    return jsonify({})


@app.route('/summary')
@login_required
def summary():
    return render_template('summary.html', user = current_user)

@app.route('/score')
@login_required
def score():
    return render_template('scores.html', user = current_user, scores = Scores.query.filter_by(userid=current_user.id).all())