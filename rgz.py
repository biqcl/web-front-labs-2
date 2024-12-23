from flask import Blueprint, render_template, request, session, current_app, redirect, url_for
from os import path
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re


rgz = Blueprint('rgz', __name__)

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


@rgz.route('/rgz/')
def main():
    return render_template('rgz/rgz.html')


@rgz.route('/rgz/login/', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users1 WHERE username = %s", (username,))
        else:
            cur.execute("SELECT * FROM users1 WHERE username = ?", (username,))

        user = cur.fetchone()
        db_close(conn, cur)
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['user_name'] = user['name']              
            return redirect(url_for('rgz.main'))
        
        else:
            error_message = "Неверный логин или пароль"

    return render_template('rgz/login.html', error_message=error_message)


@rgz.route('/rgz/register/', methods=['GET', 'POST'])
def register():
    error_message = None

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        # Валидация логина и пароля с использованием re
        if not re.match(r'^[A-Za-z0-9_.-]+$', username):
            error_message = "Логин содержит недопустимые символы"
        elif not re.match(r'^[A-Za-z0-9_.-]+$', password):
            error_message = "Пароль содержит недопустимые символы"
        else:
            hashed_password = generate_password_hash(password)
            conn, cur = db_connect()
            
            try:
                if current_app.config['DB_TYPE'] == 'postgres':
                    cur.execute("INSERT INTO users1 (name, username, password) VALUES (%s, %s, %s)", (name, username, hashed_password))
                else:
                    cur.execute("INSERT INTO users1 (name, username, password) VALUES (?, ?, ?)", (name, username, hashed_password))
                db_close(conn, cur)
                return redirect(url_for('rgz.login'))
            
            except Exception as e:
                db_close(conn, cur)
                if current_app.config['DB_TYPE'] == 'postgres' and isinstance(e, psycopg2.IntegrityError):
                    error_message = "Пользователь с таким логином уже существует"
                else:
                    error_message = "Ошибка при регистрации"

    return render_template('rgz/register.html', error_message=error_message)


@rgz.route('/rgz/logout/')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('rgz.login'))


@rgz.route('/rgz/delete_account/', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('rgz.login'))

    user_id = session.get('user_id')
    username = session.get('username')

    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM bookings WHERE user_id = %s", (user_id,))
        else:
            cur.execute("DELETE FROM bookings WHERE user_id = ?", (user_id,))

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM users1 WHERE id = %s", (user_id,))
        else:
            cur.execute("DELETE FROM users1 WHERE id = ?", (user_id,))

        conn.commit()
        
    except Exception as e:
        db_close(conn, cur)

        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32603,
                'message': str(e)
            },
            'id': None
        }
    finally:
        db_close(conn, cur)

    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('user_name', None)

    return redirect(url_for('rgz.login'))


@rgz.route('/rgz/sessions/')
def sessions():
    if 'user_id' not in session: 
        return redirect(url_for('rgz.login'))

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM sessions ORDER BY session_date, session_time")
    else:
        cur.execute("SELECT * FROM sessions ORDER BY session_date, session_time")
    
    sessions = cur.fetchall()  
    db_close(conn, cur)

    return render_template('rgz/sessions.html', sessions=sessions, session_flask=session)


@rgz.route('/rgz/session/<int:session_id>/')
def session_detail(session_id):
    if 'user_id' not in session: 
        return redirect(url_for('rgz.login'))
    
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
    else:
        cur.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    
    session_data = cur.fetchone() 

    if not session_data:
        db_close(conn, cur)
        return "Сеанс не найден", 404

    session_datetime = datetime.strptime(f"{session_data['session_date']} {session_data['session_time']}", "%Y-%m-%d %H:%M:%S")
    is_past_session = session_datetime < datetime.now()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT bookings.*, users1.name AS user_name 
            FROM bookings 
            LEFT JOIN users1 ON bookings.user_id = users1.id 
            WHERE bookings.session_id = %s
        """, (session_id,))
    else:
        cur.execute("""
            SELECT bookings.*, users1.name AS user_name 
            FROM bookings 
            LEFT JOIN users1 ON bookings.user_id = users1.id 
            WHERE bookings.session_id = ?
        """, (session_id,))

    bookings = cur.fetchall()
    db_close(conn, cur)

    return render_template('rgz/session_detail.html', session=session_data, bookings=bookings, session_flask=session, is_past_session=is_past_session)


@rgz.route('/rgz/api/book/', methods=['POST'])
def book_seat():
    data = request.json
    session_id = data['params']['session_id']
    seat_number = data['params']['seat_number']
    user_id = session.get('user_id')

    if not user_id:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Вы неавторизированы'
            },
            'id': data['id']
        }

    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
        else:
            cur.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        session_data = cur.fetchone()

        if not session_data:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 6,
                    'message': 'Сеанс не найден'
                },
                'id': data['id']
            }
        
        session_datetime = datetime.strptime(f"{session_data['session_date']} {session_data['session_time']}", "%Y-%m-%d %H:%M:%S")
        
        if session_datetime < datetime.now():
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 7,
                    'message': 'Сеанс уже прошёл'
                },
                'id': data['id']
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM bookings WHERE session_id = %s AND seat_number = %s", (session_id, seat_number))
        else:
            cur.execute("SELECT * FROM bookings WHERE session_id = ? AND seat_number = ?", (session_id, seat_number))
        booking = cur.fetchone()

        if booking:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Место уже занято'
                },
                'id': data['id']
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT COUNT(*) AS count FROM bookings WHERE session_id = %s AND user_id = %s", (session_id, user_id))
        else:
            cur.execute("SELECT COUNT(*) AS count FROM bookings WHERE session_id = ? AND user_id = ?", (session_id, user_id))
        booking_count = cur.fetchone()['count']
        
        if booking_count >= 5:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Вы можете забронировать только 5 мест на один сеанс'
                },
                'id': data['id']
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO bookings (session_id, seat_number, user_id) VALUES (%s, %s, %s)", (session_id, seat_number, user_id))
        else:
            cur.execute("INSERT INTO bookings (session_id, seat_number, user_id) VALUES (?, ?, ?)", (session_id, seat_number, user_id))
        conn.commit()

        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': data['id']
        }
    except Exception as e:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32603,
                'message': str(e)
            },
            'id': data['id']
        }
    finally:
        db_close(conn, cur)


@rgz.route('/rgz/api/get_bookings/', methods=['POST'])
def get_bookings():
    data = request.json
    session_id = data['params']['session_id']

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT bookings.*, users1.name AS user_name, users1.username 
            FROM bookings 
            LEFT JOIN users1 ON bookings.user_id = users1.id 
            WHERE bookings.session_id = %s
        """, (session_id,))
    else:
        cur.execute("""
            SELECT bookings.*, users1.name AS user_name, users1.username 
            FROM bookings 
            LEFT JOIN users1 ON bookings.user_id = users1.id 
            WHERE bookings.session_id = ?
        """, (session_id,))
    bookings = cur.fetchall()
    db_close(conn, cur)

    return {
        'jsonrpc': '2.0',
        'result': {
            'bookings': [dict(booking) for booking in bookings]
        },
        'id': data['id']
    }


@rgz.route('/rgz/api/cancel_booking/', methods=['POST'])
def cancel_booking():
    data = request.json
    session_id = data['params']['session_id']
    seat_number = data['params']['seat_number']
    user_id = session.get('user_id')
    username = session.get('username')

    if not user_id:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Вы неавторизованы'
            },
            'id': data['id']
        }

    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
        else:
            cur.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        session_data = cur.fetchone()

        if not session_data:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 6,
                    'message': 'Сеанс не найден'
                },
                'id': data['id']
            }

        session_datetime = datetime.strptime(f"{session_data['session_date']} {session_data['session_time']}", "%Y-%m-%d %H:%M:%S")
        if session_datetime < datetime.now():
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 7,
                    'message': 'Сеанс уже прошёл'
                },
                'id': data['id']
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM bookings WHERE session_id = %s AND seat_number = %s", (session_id, seat_number))
        else:
            cur.execute("SELECT * FROM bookings WHERE session_id = ? AND seat_number = ?", (session_id, seat_number))
        booking = cur.fetchone()

        if not booking:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Бронь не найдена'
                },
                'id': data['id']
            }

        if booking['user_id'] != user_id and username != 'admin':
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'У вас нет прав на внесение изменений'
                },
                'id': data['id']
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM bookings WHERE session_id = %s AND seat_number = %s", (session_id, seat_number))
        else:
            cur.execute("DELETE FROM bookings WHERE session_id = ? AND seat_number = ?", (session_id, seat_number))
        conn.commit()
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': data['id']
        }
    except Exception as e:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32603,
                'message': str(e)
            },
            'id': data['id']
        }
    finally:
        db_close(conn, cur)


@rgz.route('/rgz/admin/edit_session/<int:session_id>/', methods=['GET', 'POST'], endpoint='admin_edit_session')
def edit_session(session_id):
    if session.get('username') != 'admin':
        return redirect(url_for('rgz.login'))
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
    else:
        cur.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    session_data = cur.fetchone()  

    if not session_data:
        db_close(conn, cur)
        return "Сеанс не найден", 404

    session_datetime = datetime.strptime(f"{session_data['session_date']} {session_data['session_time']}", "%Y-%m-%d %H:%M:%S")
    if session_datetime < datetime.now():
        db_close(conn, cur)
        return redirect(url_for('rgz.session_detail', session_id=session_id))

    if request.method == 'POST':
        movie_name = request.form['movie_name']
        session_date = request.form['session_date']
        session_time = request.form['session_time']

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE sessions SET movie_name = %s, session_date = %s, session_time = %s WHERE id = %s", (movie_name, session_date, session_time, session_id))
        else:
            cur.execute("UPDATE sessions SET movie_name = ?, session_date = ?, session_time = ? WHERE id = ?", (movie_name, session_date, session_time, session_id))
        db_close(conn, cur)
        return redirect(url_for('rgz.sessions'))
    
    db_close(conn, cur)
    return render_template('rgz/edit_session.html', session=session_data)


@rgz.route('/rgz/admin/delete_session/<int:session_id>/', methods=['POST'], endpoint='admin_delete_session')
def delete_session(session_id):
    if session.get('username') != 'admin':
        return redirect(url_for('rgz.login'))
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
    else:
        cur.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    session_data = cur.fetchone()

    if not session_data:
        db_close(conn, cur)
        return "Сеанс не найден", 404

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
    else:
        cur.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    db_close(conn, cur)
    
    return redirect(url_for('rgz.sessions'))


@rgz.route('/rgz/admin/add_session/', methods=['GET', 'POST'], endpoint='admin_add_session')
def add_session():
    if session.get('username') != 'admin':
        return redirect(url_for('rgz.login'))
    
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        session_date = request.form['session_date']
        session_time = request.form['session_time']
        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO sessions (movie_name, session_date, session_time) VALUES (%s, %s, %s)", (movie_name, session_date, session_time))
        else:
            cur.execute("INSERT INTO sessions (movie_name, session_date, session_time) VALUES (?, ?, ?)", (movie_name, session_date, session_time))
        
        db_close(conn, cur)
        return redirect(url_for('rgz.sessions'))
    return render_template('rgz/add_session.html')


@rgz.route('/rgz/admin/remove_booking/<int:session_id>/<int:seat_number>/', methods=['POST'], endpoint='admin_remove_booking')
def remove_booking(session_id, seat_number):
    if session.get('username') != 'admin':
        return redirect(url_for('rgz.login'))
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM bookings WHERE session_id = %s AND seat_number = %s", (session_id, seat_number))
    else:
        cur.execute("DELETE FROM bookings WHERE session_id = ? AND seat_number = ?", (session_id, seat_number))
   
    db_close(conn, cur)
    return redirect(url_for('rgz.session_detail', session_id=session_id))
