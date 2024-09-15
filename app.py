from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
   return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <style>
            header {
                background-color: #6B2137;
                color: #F9EEE5;
                padding: 5px;
                font-size: 12pt; 
                text-align: left;
            }
            footer {
                background-color: #6B2137;
                color: #F9EEE5;
                padding: 5px;
                text-align: right;
                position: fixed;
                bottom: 0px;
                right: 0px;
                left: 0px;
            }
            body{
                background-color: #F9EEE5;
                color: #6B2137;
                margin: 0px;
            }            
            a {
                padding: 10px;
                text-decoration: none;
                color: #D0C360;
                font-size: 14pt;
                font-weight: bold;
            }  
        </style>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование часть 2. Список лабораторных
        </header>

        <a href="/lab1">Первая лабораторная</a>

        <footer>
            &copy; Бызова Мария, ФБИ-22, 3 курс, 2024
        </footer>
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
               <a href="/lab1/web">web</a>
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
        <img src="'''+ path +'''">
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
    </body>
</html>
'''

@app.errorhandler(404)
def not_found(err):
    return "Такой страницы не существует...", 404
