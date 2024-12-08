import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from flask import  render_template, Blueprint, request, jsonify, current_app
from datetime import datetime

lab7 = Blueprint('lab7', __name__)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'maria_byzova_knowledge_base',
            user = 'maria_byzova_knowledge_base',
            password = '1304'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films ORDER BY id")
    else:
        cur.execute("SELECT * FROM films ORDER BY id")
    films = cur.fetchall()
    db_close(conn, cur)
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    if film is None:
        return 'Такого фильма нет :(', 404
    return jsonify(film)


@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM films WHERE id = %s", (id,))
    else:
        cur.execute("DELETE FROM films WHERE id = ?", (id,))
    rows_affected = cur.rowcount
    db_close(conn, cur)
    if rows_affected == 0:
        return 'Такого фильма нет :(', 404
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['PUT'])
def put_film(id):
    conn, cur = db_connect()
    film = request.get_json()

    if 'title_ru' in film and film['title_ru'] and not film['title']:
        film['title'] = film['title_ru']

    errors = {}

    if film['title_ru'] == '':
        errors['title_ru'] = 'Заполните название на русском'

    if film['title'] == '':
        errors['title'] = 'Заполните название или добавьте название на русском'

    if film['year'] == '' or not isinstance(film['year'], (int, float)):
        errors['year'] = 'Заполните год выхода фильма'
    else:
        current_year = datetime.now().year
        if not 1895 <= film['year'] <= current_year:
            errors['year'] = f'Год должен быть от 1895 до {current_year}'

    if film['description'] == '':
        errors['description'] = 'Заполните описание'
    else:
        if len(film['description']) > 2000:
            errors['description'] = 'Описание не должно превышать 2000 символов'

    if errors:
        db_close(conn, cur)
        return jsonify(errors), 400
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE films
                SET title = %s, title_ru = %s, year = %s, description = %s
                WHERE id = %s
            """, (film['title'], film['title_ru'], film['year'], film['description'], id))
        else:
            cur.execute("""
                UPDATE films
                SET title = ?, title_ru = ?, year = ?, description = ?
                WHERE id = ?
            """, (film['title'], film['title_ru'], film['year'], film['description'], id))
        rows_affected = cur.rowcount
        db_close(conn, cur)
        if rows_affected == 0:
            return 'Такого фильма нет :(', 404
        return jsonify(film)


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    conn, cur = db_connect()
    film = request.get_json()

    if film['title_ru'] and not film['title']:
        film['title'] = film['title_ru']

    errors = {}

    if film['title_ru'] == '':
        errors['title_ru'] = 'Заполните название на русском'

    if film['title'] == '':
        errors['title'] = 'Заполните название или добавте название на русском'
    

    if film['year'] == '' or not isinstance(film['year'], (int, float)):
        errors['year'] = 'Заполните год выхода фильма'
    else:
        current_year = datetime.now().year
        if not 1895 <= film['year'] <= current_year:
            errors['year'] = f'Год должен быть от 1895 до {current_year}'

    if film['description'] == '':
        errors['description'] = 'Заполните описание'
    else:
        if len(film['description']) > 2000:
            errors['description'] = 'Описание не должно превышать 2000 символов'

    if errors:
        db_close(conn, cur)
        return jsonify(errors), 400
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO films (title, title_ru, year, description)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (film['title'], film['title_ru'], film['year'], film['description']))
            id = cur.fetchone()['id']
        else:
            cur.execute("""
                INSERT INTO films (title, title_ru, year, description)
                VALUES (?, ?, ?, ?)
            """, (film['title'], film['title_ru'], film['year'], film['description']))
            cur.execute("SELECT last_insert_rowid()")
            id = cur.fetchone()[0]
        db_close(conn, cur)
        return jsonify({'id': id}), 201
        