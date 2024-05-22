"""
Задание №2.
Создать базу данных для хранения информации о книгах в библиотеке.
База данных должна содержать две таблицы: "Книги" и "Авторы".
В таблице "Книги" должны быть следующие поля: id, название, год издания,
количество экземпляров и id автора.
В таблице "Авторы" должны быть следующие поля: id, имя и фамилия.
Необходимо создать связь между таблицами "Книги" и "Авторы".
Написать функцию-обработчик, которая будет выводить список всех книг с
указанием их авторов.
"""
import random
from flask import Flask, render_template
from model.models_lib import db, Book, Author

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)


@app.route('/')
def index():
    books = Book.query.all()  # Получаем все книги из базы данных
    return render_template('Task2/index.html', books=books, title='Библиотека')


@app.route('/data/')
def data():
    return render_template('Task2/data.html', title='О мне')


@app.route('/authors/')
def authors_page():
    authors = Author.query.all()
    return render_template(
        'Task2/authors.html', authors=authors)


def generate_random_title():
    # Создаем объект Book с рандомными значениями
    book = Book(title="Title", year=random.randint(1900, 2023),
                copies=random.randint(1, 1000),
                author=generate_random_author())
    return book


def generate_random_author():
    first_names = ['John', 'Anna', 'Peter', 'Jane', 'Mary']
    last_names = ['Doe', 'Smith', 'Jones', 'White', 'Black']
    return f"{random.choice(first_names)} {random.choice(last_names)}"


@app.cli.command('init-db')
def initdb_command():
    db.create_all()
    print('Initialized the database.')


@app.cli.command('fill-db')
def fill_db():
    count = 10
    for _ in range(count):
        new_author = Author(
            first_name=generate_random_author(),
            last_name=generate_random_author()
        )
        db.session.add(new_author)
        db.session.commit()  # Добавлено добавление и коммит автора
    db.session.commit()  # Добавлен дополнительный коммит для фиксации изменений


@app.cli.command('fill-book')
def book():
    books = [
        Book(title="Harry Potter and the Philosopher's Stone", year=2001, copies=1000, author_id=1),
        Book(title="The Lord of the Rings", year=1954, copies=500, author_id=2),
        # Добавьте больше книг по аналогии
    ]
    db.session.add_all(books)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
