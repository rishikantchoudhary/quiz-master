from flask_sqlalchemy import SQLAlchemy
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy(app)

# models

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    passhash = db.Column(db.String(256), nullable=False)
    fullname = db.Column(db.String(80), nullable=False)
    qualification = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.passhash, password)

class Subjects(db.Model):
    __tablename__ = 'subjects'
    subjectid = db.Column(db.Integer, primary_key=True)
    subjectname = db.Column(db.String(80), unique=False, nullable=False)
    subjectdesc = db.Column(db.String(512), nullable=False)
    #relationships
    chapters = db.relationship('Chapters', backref='subject', lazy=True)

class Chapters(db.Model):
    __tablename__ = 'chapters'
    chapterid = db.Column(db.Integer, primary_key=True)
    subjectid = db.Column(db.Integer, db.ForeignKey('subjects.subjectid'), nullable=False)
    chaptername = db.Column(db.String(80), unique=False, nullable=False)
    chapterdesc = db.Column(db.String(512), nullable=False)
    #relationships
    questions = db.relationship('Questions', backref='chapter', lazy=True)

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
    # create admin if does not exist
    admin = User.query.filter_by(is_admin= True).first()
    if not admin:
        import datetime
        dob = datetime.date(2000, 1, 1)
        admin = User(username='admin', password='admin', fullname='Admin', qualification='phd', dob=dob , is_admin=True)
        db.session.add(admin)
        quiz1 = Quizzes(quizname='quiz1', subjectid=1, duration=30, quizdate=datetime.date(2021, 1, 1))
        quiz2 = Quizzes(quizname='quiz2', subjectid=2, duration=30, quizdate=datetime.date(2021, 1, 1))
        db.session.add(quiz1)
        db.session.add(quiz2)
        db.session.commit()