"""
Задание №8.
Создать форму для регистрации пользователей на сайте.
Форма должна содержать поля "Имя", "Фамилия", "Email",
"Пароль" и кнопку "Зарегистрироваться".
При отправке формы данные должны сохраняться в базе
данных, а пароль должен быть зашифрован.
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, url_for
from flask_wtf import CSRFProtect

from model.forms import RegistrationForm
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

from model.models import User

db.create_all()


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = form.password.data  # Placeholder for password hashing
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # db.create_all()
        return redirect(url_for('success'))
    return render_template('Task8/register.html', form=form)


@app.route('/success')
def success():
    return "Registration successful! 🎉"


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
