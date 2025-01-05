from flask import Flask, render_template, request, redirect, url_for

from app import app
from models import db, User, Subjects, Chapters, Quizzes, Questions

@app.route('/')
def signup():
    return render_template('signup.html')

# @app.route('/', methods=['POST'])
# def signup_post():
    # username = request.form.get('username')
    # password = request.form.get('password')
    # full_name = request.form.get('full-name')
    # qualification = request.form.get('qualification')
    # dob = request.form.get('dob')

    # user = User(username=username, password=password, full_name=full_name, qualification=qualification, dob=dob)
    # db.session.add(user)
    # db.session.commit()
    # return redirect(url_for('login'))
    

@app.route('/login')
def login():
    return render_template('login.html')