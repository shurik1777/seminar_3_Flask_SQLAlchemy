"""
Задание
Создать форму для регистрации пользователей на сайте.
Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль"
и кнопку "Зарегистрироваться".
При отправке формы данные должны сохраняться в базе данных,
а пароль должен быть зашифрован.
"""
from flask import Flask
from flask import render_template, request, redirect, url_for, flash

from model.model_reg import db, User
from model.forms import RegistrationForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db.init_app(app)

app.config["SECRET_KEY"] = (
    "aff4028c6c00ebgjfjb488eb83149bb1af1c427c85715c022b9"
)
csrf = CSRFProtect(app)


@app.cli.command('db-init')
def init_db():
    db.create_all()


@app.route('/')
@app.route('/index/')
def index():
    return render_template('Task8/index.html', title='Главная')


@app.route('/data/')
def data():
    return render_template('Task8/data.html', title='О мне')


@app.route("/registration/", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    context = {"title": "Страница регистрации", "form": form}
    if request.method == "POST" and form.validate():
        with app.app_context():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data

            secret_password = generate_password_hash(form.password.data)

            user = User.query.filter_by(email=email).first()
            if user:
                flash(
                    "Пользователь с такой электронной почтой уже зарегистрирован!", "danger"
                )
                return redirect(url_for("registration"))

            new_user = User(first_name=first_name, last_name=last_name, email=email, password=secret_password)
            db.session.add(new_user)
            db.session.commit()

        flash(f"Здравствуйте {first_name} {last_name}!Вы успешно зарегистрированы!!!", "success")
        return redirect(url_for("index"))

    return render_template("Task8/register.html", **context)


if __name__ == '__main__':
    app.run(debug=True)
