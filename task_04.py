from flask import Flask, render_template, redirect, url_for, flash,request
from model.model_reg import db, User, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)


@app.route('/')
def index():
    return render_template('Task4/index.html', title='Главная')


@app.route('/data/')
def data():
    return render_template('Task4/data.html', title='О мне')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        with app.app_context():
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Имя пользователя уже существует!', 'error')
                return redirect(url_for('register'))

            existing_email = User.query.filter_by(email=form.email.data).first()
            if existing_email:
                flash('Электронная почта уже существует!', 'error')
                return redirect(url_for('register'))

            new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Пользователь успешно зарегистрирован!', 'success')
            return redirect(url_for('login'))

    return render_template('Task4/register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль!', 'error')
            return redirect(url_for('login'))
    return render_template('Task4/login.html', title='Вход')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
