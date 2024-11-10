from flask import  render_template, Blueprint, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template ('lab5/lab5.html', login=session.get('login'))


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


@lab5.route('/lab5/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля!')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login, ))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template ('lab5/register.html', error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password_hash))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error='Заполните поля')
    
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'],password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)


@lab5.route('/lab5/create/', methods = ['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
       error = "Название статьи и текст не могут быть пустыми."
       return render_template('lab5/create_article.html', error=error, title=title)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

    user_id = cur.fetchone()["id"]


    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles(user_id, title, article_text) \
                    VALUES (%s, %s, %s)", (user_id, title, article_text))
    else:
        cur.execute("INSERT INTO articles(user_id, title, article_text) \
                    VALUES (?, ?, ?)", (user_id, title, article_text))
    # cur.fetchone()

    db_close(conn, cur)
    return redirect('/lab5/')


@lab5.route('/lab5/list/') 
def lists():
  login = session.get('login')
  if not login:
    return redirect('/lab5/login')
  
  conn, cur = db_connect()

  if current_app.config['DB_TYPE'] == 'postgres':
    cur.execute("SELECT id FROM users WHERE login=%s;", (login, ))
  else:
    cur.execute("SELECT id FROM users WHERE login=?;", (login, ))

  user_id = cur.fetchone()["id"]

  # Изменено: добавлено условие для типа данных
  if current_app.config['DB_TYPE'] == 'postgres':
    cur.execute(
      "SELECT * FROM articles WHERE user_id=%s ORDER BY CASE WHEN is_favorite THEN 0 ELSE 1 END, id ASC;",
      (user_id, )
    )
  else:
    cur.execute(
      "SELECT * FROM articles WHERE user_id=? ORDER BY CASE WHEN is_favorite THEN 0 ELSE 1 END, id ASC;",
      (user_id, )
    ) 
  articles = cur.fetchall()

  db_close(conn, cur)

  if not articles:
    message = "У вас еще нет ни одной статьи :("
  else:
    message = None

  return render_template('/lab5/articles.html', articles=articles, message=message)


@lab5.route('/lab5/logout/', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab5/')


@lab5.route('/lab5/edit/<int:article_id>/', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('article_text')
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, text, article_id))
        else:
            cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, text, article_id))
        
        conn.commit()
        db_close(conn, cur)
        
        return redirect('/lab5/list/')
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id, ))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id, ))

    article = cur.fetchone()
    db_close(conn, cur)
    
    return render_template('/lab5/edit_article.html', article=article)


@lab5.route('/lab5/delete/<int:article_id>/')
def delete_article(article_id):
    login = session.get('login')

    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id, ))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id, ))

    db_close(conn, cur)
    
    return redirect('/lab5/list/')


@lab5.route('/lab5/users/')
def list_users():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users;")
    else:
        cur.execute("SELECT login FROM users;")

    users = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/favorite/<int:article_id>/', methods=['POST'])
def favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET is_favorite=TRUE WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("UPDATE articles SET is_favorite=TRUE WHERE id=? AND user_id=?;", (article_id, user_id))

    db_close(conn, cur)

    return redirect('/lab5/list/')


@lab5.route('/lab5/unfavorite/<int:article_id>/', methods=['POST'])
def unfavorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET is_favorite=FALSE WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("UPDATE articles SET is_favorite=FALSE WHERE id=? AND user_id=?;", (article_id, user_id))

    db_close(conn, cur)

    return redirect('/lab5/list/')


@lab5.route('/lab5/make_public/<int:article_id>/', methods=['POST'])
def make_public(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET is_public='t' WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("UPDATE articles SET is_public='t' WHERE id=? AND user_id=?;", (article_id, user_id))

    db_close(conn, cur)

    return redirect('/lab5/list/')

@lab5.route('/lab5/make_private/<int:article_id>/', methods=['POST'])
def make_private(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user_id = cur.fetchone()["id"]

    cur.execute("UPDATE articles SET is_public='f' WHERE id=%s AND user_id=%s;", (article_id, user_id))

    db_close(conn, cur)

    return redirect('/lab5/list/')



@lab5.route('/lab5/public_articles/')
def public_articles():
    conn, cur = db_connect()

    cur.execute("SELECT * FROM articles WHERE is_public='t' ORDER BY id ASC;")
    public_articles = cur.fetchall()
    db_close(conn, cur)

    return render_template('/lab5/public_articles.html', public_articles=public_articles)
