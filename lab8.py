import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from flask import  render_template, Blueprint, request, current_app, redirect, session
from db import db
from db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user


lab8 = Blueprint('lab8', __name__)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'maria_byzova_orm',
            user = 'maria_byzova_orm',
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


@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', login=current_user.login if current_user.is_authenticated else None)


@lab8.route('/lab8/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    login_error = ""
    password_error = ""

    if login_form is None: 
        login_error = "Введите логин!"
    if password_form is None: 
        password_error = "Введите пароль!"

    if login_error or password_error:
        return render_template('lab8/register.html', login_error=login_error, password_error=password_error)
    
    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()

    new_user = users.query.filter_by(login=login_form).first()
    login_user(new_user, remember=False)
    return redirect('/lab8/') 


@lab8.route('/lab8/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    login_error = ""
    password_error = ""

    if login_form == "":
        login_error = "Введите логин!"
    if password_form =="":
        password_error = "Введите пароль!"

    if login_error or password_error:
        return render_template('lab8/register.html', login_error=login_error, password_error=password_error)
        
    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember = False)
            return redirect('/lab8/')        
   
    return render_template('/lab8/login.html', error = 'Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "Список статей"


@lab8.route('/lab8/logout/', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')
