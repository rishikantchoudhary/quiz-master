from flask_sqlalchemy import SQLAlchemy
from app import app
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

# models

class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    passhash = db.Column(db.String(256), nullable=False)
    fullname = db.Column(db.String(80), nullable=False)
    qualification = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date, nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

class Subjects(db.Model):
    __tablename__ = 'subjects'
    subjectid = db.Column(db.Integer, primary_key=True)
    subjectname = db.Column(db.String(80), unique=False, nullable=False)
    subjectdesc = db.Column(db.String(512), nullable=False)

class Chapters(db.Model):
    __tablename__ = 'chapters'
    chapterid = db.Column(db.Integer, primary_key=True)
    subjectid = db.Column(db.Integer, db.ForeignKey('subjects.subjectid'), nullable=False)
    chaptername = db.Column(db.String(80), unique=False, nullable=False)
    chapterdesc = db.Column(db.String(512), nullable=False)

class Quizzes(db.Model):
    __tablename__ = 'quizzes'
    quizid = db.Column(db.Integer, primary_key=True)
    quizname = db.Column(db.String(80), unique=False, nullable=False)
    subjectid = db.Column(db.Integer, db.ForeignKey('subjects.subjectid'), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    quizdate = db.Column(db.Date, nullable=False)

class Questions(db.Model):
    __tablename__ = 'questions'
    questionid = db.Column(db.Integer, primary_key=True)
    quizid = db.Column(db.Integer, db.ForeignKey('quizzes.quizid'), nullable=False)
    chapterid = db.Column(db.Integer, db.ForeignKey('chapters.chapterid'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    statement = db.Column(db.String(512), nullable=False)
    option1 = db.Column(db.String(80), nullable=False)
    option2 = db.Column(db.String(80), nullable=False)
    option3 = db.Column(db.String(80), nullable=False)
    option4 = db.Column(db.String(80), nullable=False)
    ans = db.Column(db.Integer, nullable=False)

# create database if does not exist

with app.app_context():
    db.create_all()