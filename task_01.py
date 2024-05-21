"""
Задание №1.
Создать базу данных для хранения информации о студентах университета.
База данных должна содержать две таблицы: "Студенты" и "Факультеты".
В таблице "Студенты" должны быть следующие поля: id, имя, фамилия,
возраст, пол, группа и id факультета.
В таблице "Факультеты" должны быть следующие поля: id и название
факультета.
Необходимо создать связь между таблицами "Студенты" и "Факультеты".
Написать функцию-обработчик, которая будет выводить список всех
студентов с указанием их факультета.
"""

from flask import Flask, render_template
from model.models_one import Gender, db, Student, Faculty
from random import choice, randint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase_sem3_1.db'
db.init_app(app)


@app.route('/')
def index():
    return render_template('Task1/index.html', title='Главная')


@app.route('/data/')
def data():
    return render_template('Task1/data.html', title='О мне')


@app.route('/students/')
def students():
    students = db.session.query(Student).all()
    return render_template('Task1/students.html', student=students, title='Students')


@app.cli.command('init-db')
def initdb_command():
    db.create_all()
    print('Initialized the database.')


@app.cli.command('fill-db')
def fill_db():
    # Добавляем студентов
    count = 10
    for student in range(1, count + 1):
        new_student = Student(
            name=f'student{student}', last_name=f'last_name{student}',
            age=choice([student, student * 5]),
            gender=choice([Gender.male, Gender.female]), group=f'group{student}',
            faculty_id=randint(1, 10)
        )
        db.session.add(new_student)
    db.session.commit()

    # Добавляем факультеты
    for faculty in range(1, count):
        new_faculty = Faculty(faculty_name=f'faculty{faculty}')
        db.session.add(new_faculty)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
