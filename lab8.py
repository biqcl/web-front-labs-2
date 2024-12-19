import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from flask import  render_template, Blueprint, request, current_app, redirect, session, url_for
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

    if login_form == '': 
        login_error = "Введите логин!"
    if password_form == '': 
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
    remember = request.form.get('remember') 

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
            login_user(user, remember=(remember == 'on'))
            return redirect('/lab8/')        
   
    return render_template('/lab8/login.html', error = 'Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)


@lab8.route('/lab8/logout/', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/create_article/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_favorite = request.form.get('is_favorite') == 'on'
        is_public = request.form.get('is_public') == 'on'

        if not current_user.is_authenticated:
            return redirect(url_for('lab8.login'))

        new_article = articles(
            login_id=current_user.id,
            title=title,
            article_text=article_text,
            is_favorite=is_favorite,
            is_public=is_public,
            likes=0
        )
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('lab8.article_list'))

    return render_template('lab8/create_article.html')


@lab8.route('/lab8/edit_article/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return "У вас нет прав на редактирование этой статьи", 403

    if request.method == 'POST':
        article.title = request.form.get('title')
        article.article_text = request.form.get('article_text')
        article.is_favorite = request.form.get('is_favorite') == 'on'
        article.is_public = request.form.get('is_public') == 'on'

        db.session.commit()
        return redirect(url_for('lab8.article_list'))

    return render_template('lab8/edit_article.html', article=article)


@lab8.route('/lab8/all_articles/')
@login_required
def all_articles():
    all_articles = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/all_articles.html', articles=all_articles)


@lab8.route('/lab8/delete_article/<int:article_id>/', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return "У вас нет прав на удаление этой статьи", 403

    db.session.delete(article)
    db.session.commit()

    return redirect(url_for('lab8.article_list'))


@lab8.route('/lab8/search', methods=['GET'])
def search_articles():
    query = request.args.get('query')
    if not query:
        return redirect('/lab8/articles/')
    search_results = articles.query.filter((articles.title.ilike(f'%{query}%')) | (articles.article_text.ilike(f'%{query}%'))).all()
    return render_template('lab8/search_results.html', query=query, articles=search_results)
