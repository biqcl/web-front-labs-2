import os
from flask import Flask, url_for
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')


app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)


@app.route("/")
@app.route("/index")
def index():
   path = url_for("static", filename="main.css")
   fav = url_for("static", filename="fav.png")
   return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" type="text/css" href="''' + path + '''">
        <link rel="shortcut icon" href="''' + fav + '''">
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование часть 2. Список лабораторных
        </header>
        <br><a href="/lab1">&#10023; Первая лабораторная</a>
        <br><a href="/lab2">&#10023; Вторая лабораторная</a>
        <br><a href="/lab3">&#10023; Третья лабораторная</a>
        <br><a href="/lab4">&#10023; Четвёртая лабораторная</a>
        <br><a href="/lab5">&#10023; Пятая лабораторная</a>
        <br><a href="/lab6">&#10023; Шестая лабораторная</a>
        <br><a href="/lab6">&#10023; Седьмая лабораторная</a>

        <footer>
            &copy; Бызова Мария, ФБИ-22, 3 курс, 2024
        </footer>
    </body>
</html>
'''


@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename="error.jpeg")
    return '''
<!doctype html>
<html>
    <head>
        <style>
            img {
                width: 55%;
            }
            body {
                color: red;
                font-weight: bold;
                font-size: 24pt;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <p>Такой страницы не существует!! Попробуйте в другой раз :)</p><br>
        <img src="'''+ path +'''"><br>
    </body>
</html>
''', 404


@app.errorhandler(500)
def internal_server(error):
    return '''
<!doctype html>
<html>
    <head>
        <style>
            body {
                margin-top: 18%;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                text-align: center;
            }
            h1 {
                color: red;
                font-weight: bold;
                font-size: 24pt;                
            }
            p {
                color: grey;
                font-size: 14pt;
            }
        </style>
    </head>
    <body>
        <div>
            <h1>На сервере произошла ошибка :(</h1>
            <p>Попробуйте зайти на страницу позже!!</p>
        </div>
    </body>
</html>
''', 500
      