import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Gender(enum.Enum):
    male = 'Муж'
    female = 'Жен'


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty_name = db.Column(db.String(80), nullable=False)
    student = db.relationship('Student', backref=db.backref(f'faculty'), lazy=True)

    def __repr__(self):
        return f'Faculty({self.faculty_name})'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    group = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    grades = db.relationship('Grade', backref='student', lazy=True)

    def __repr__(self):
        return f'Student({self.name}, {self.last_name})'


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_name = db.Column(db.String(80), nullable=False)
    grade = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Grade({self.subject_name}, {self.grade})'
