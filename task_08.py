"""
Задание №8.
Создать форму для регистрации пользователей на сайте.
Форма должна содержать поля "Имя", "Фамилия", "Email",
"Пароль" и кнопку "Зарегистрироваться".
При отправке формы данные должны сохраняться в базе
данных, а пароль должен быть зашифрован.
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


from model.models import User

app = Flask(__name__)
load_dotenv()  # Автоматически загружает переменные окружения из .env.

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('Task8/index.html',
                           title='Стартовая страница')


@app.route('/data')
def data():
    return render_template('Task8/data.html',
                           title='Информация')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']

        if not name or not surname or not email or not password:
            flash('Все поля должны быть заполнены', 'error')
            return redirect(url_for('register'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email уже зарегистрирован', 'error')
            return redirect(url_for('register'))

        user = User(name=name, surname=surname, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно', 'success')
        return redirect(url_for('login'))
    return render_template('Task8/register.html')


if __name__ == '__main__':
    app.run(debug=True)
