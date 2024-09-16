from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
   path = url_for("static", filename="styles.css")
   return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" type="text/css" href="''' + path + '''">
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование часть 2. Список лабораторных
        </header>
        <br><a href="/lab1">&#10023; Первая лабораторная</a>

        <footer>
            &copy; Бызова Мария, ФБИ-22, 3 курс, 2024
        </footer>
    </body>
</html>
'''
@app.route("/lab1")
def lab1():
    path = url_for("static", filename="styles.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + path + '''">
        <title>Лабораторная 1</title>
    </head>
    <body>
        <div>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </div>
        <a href="/lab1/web">web</a><br>
        <a href="/lab1/author">author</a><br>
        <a href="/lab1/oak">oak</a><br>
        <a href="/lab1/counter">counter</a><br>
        <a href="/lab1/reset">reset</a><br>
        <a href="/lab1/info">info</a><br>
        <a href="/lab1/created">created</a><br>
        <a href="/lab1/errors">errors</a><br>
        <a href="/">&#8656;</a>
    </body>
</html>
'''

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }

@app.route("/lab1/author")
def author():
    name = "Бызова Мария Максимовна"
    group = "ФБИ-22"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
           <body>
               <p>Студентка: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href="/lab1/web">web</a><br>
               <a href="/lab1">&#8656;</a>
           </body>
        </html>"""

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    path1 = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + path1 + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="'''+ path +'''"><br>
        <a href="/lab1">&#8656;</a>
    </body>
</html>
'''

count = 0

@app.route("/lab1/counter")
def counter():
    global count
    count +=1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: '''+ str(count) +'''
        <br><a href="/lab1/reset">Очистить счётчик</a><br>
        <a href="/lab1">&#8656;</a>
    </body>
</html>
'''

@app.route("/lab1/reset")
def reset():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        <a href="/lab1/counter">Очищенный счётчик</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info(): 
   return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
   return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div>Что-то создано...</div>
        <a href="/lab1">&#8656;</a>
    </body>
</html>
'''
@app.route("/lab1/errors")
def errors():
   return '''
<!doctype html>
<html>
    <body>
        <a href="/lab1/bad_request">400;</a><br>
        <a href="/lab1/unauthorized">401;</a><br>
        <a href="/lab1/payment_required">402;</a><br>
        <a href="/lab1/forbidden">403;</a><br>
        <a href="/lab1/not_found">404;</a><br>
        <a href="/lab1/method_not_allowed">405;</a><br>
        <a href="/lab1/teapot">418;</a><br>
        <a href="/lab1">&#8656;</a>
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


@app.route("/lab1/bad_request")
def bad_request():
    return "Ошибка 400. Неправильный синтаксис", 400

@app.route("/lab1/unauthorized")
def unauthorized():
    return "Ошибка 401. Неавторизованный доступ", 401

@app.route("/lab1/payment_required")
def payment_required():
    return "Ошибка 402. Требуется оплата", 402

@app.route("/lab1/forbidden")
def forbidden():
    return "Ошибка 403. Доступ запрещён", 403

@app.route("/lab1/method_not_allowed")
def method_not_allowed():
    return "Ошибка 405. Метод не поддерживается целевым ресурсом", 405

@app.route("/lab1/teapot")
def teapot():
    return "Ошибка 418. Сервер не может приготовить кофе, потому что он чайник", 418
