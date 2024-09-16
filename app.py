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
            <b>Flask</b> — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </div>

        <h2>Список роутов</h2>
        <div class="link">
            <a href="/lab1/web">web</a><br>
            <a href="/lab1/author">author</a><br>
            <a href="/lab1/oak">oak</a><br>
            <a href="/lab1/counter">counter</a><br>
            <a href="/lab1/reset">reset</a><br>
            <a href="/lab1/info">info</a><br>
            <a href="/lab1/created">created</a><br>
            <a href="/lab1/errors">errors</a><br>
            <a href="/lab1/headers">headers</a><br>
            <a href="/">&#8656;</a>
        </div>
    </body>
</html>
'''

@app.route("/lab1/web")
def web():
    return '''
<!doctype html>
<html>
    <body>
        <h1>web-сервер на flask</h1>
        <a href="/author">author</a>
    </body>
</html>''', 200, {
    'X-Server': 'sample',
    'Content-Type': 'text/plain; charset=utf-8'
    }

@app.route("/lab1/author")
def author():
    name = "Бызова Мария Максимовна"
    group = "ФБИ-22"
    faculty = "ФБ"
    return """
<!doctype html>
<html>
    <body>
        <p>Студентка: """ + name + """</p>
        <p>Группа: """ + group + """</p>
        <p>Факультет: """ + faculty + """</p>
        <a href="/lab1/web">web</a><br>
        <a href="/lab1">&#8656;</a>
    </body>
</html>
"""

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
        <a href="/lab1/internal_server_error">500;</a><br>
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

@app.route('/lab1/internal_server_error')
def internal_server_error():
    result = 10 / 0  
    return 'Результат: ' + str(result)

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

@app.route("/lab1/headers")
def headers():
    path = url_for("static", filename="pngegg.png")
    return '''
<!doctype html>
<html>
<head>
    <style>
        img {
            width: 100%;
        }
        body {
            background: linear-gradient(#B7D8FF, #dcffb7);
            margin: 0;
        }
        h1, h2, div {
            margin: 10px;
            text-align: justify;
            color: #042c5e;
        }
        h1, h2 {
            text-align: center;
        }
    </style>
</head>
    <body>        
        <h1>Таинственный сад</h1>
        <h2>Фрэнсис Элиза Ходжсон Бёрнетт</h2>
        <div>
            Когда Мэри Леннокс только что появилась в Мисселтуэйт Мэноре – Йоркширском поместье дяди, выглядела она прескверно,
            да и вела себя не очень-то хорошо. Вообразите надменную девочку десяти лет с худеньким злым лицом и тщедушным телом,
            добавьте к этому болезненную желтизну кожи, и вы без труда поймете, почему никого в Мисселтуэйте ее присутствие не 
            порадовало.
        </div>
        <div>
            До недавнего времени Мэри жила в Индии. Там ее с самого рождения преследовали болезни. Отец Мэри, чиновник 
            Британского правительственного департамента, тоже часто болел, а в промежутках с головой погружался в работу. 
            Мать Мэри, в противоположность мужу и дочери, славилась здоровьем, красотой и общительностью. Она часто повторяла,
            что без общества интересных и веселых людей не выдержала бы в Индии даже дня. Миссис Леннокс совсем не хотела 
            обременять свою жизнь детьми. Когда же Мэри все-таки появилась на свет, ее тут же препоручили заботам няни-индуски,
            или, по-местному, Айе. Няне было весьма доходчиво объяснено, что чем реже ребенок будет попадаться на глаза 
            Мэмсахибе (госпоже), тем больше оценят ее работу. С тех пор девочку держали на расстоянии от родителей. 
            Мэри росла, стала ходить, заговорила, мало-помалу превращалась во вполне сознательное существо, но родители 
            так и не приблизили ее к себе.
        </div>
        <div>
            Боясь гнева хозяйки, слуги разрешали девочке делать все, что угодно, только бы та не скандалила. Это не замедлило 
            принести плоды. К шести годам Мэри стала настоящим тираном и понукала слугами, как могла. Молодая гувернантка, 
            которую родители выписали для Мэри из Англии, уволилась через три месяца. Другие гувернантки требовали расчета 
            гораздо скорее. Если бы Мэри в конце концов вдруг не захотелось самой научиться грамоте, вероятнее всего, она 
            вообще не смогла бы читать и писать.
        </div>
        <div>
            Так длилось из года в год все девять лет ее жизни, пока не наступило утро, которое Мэри встретила в особенно 
            дурном настроении. Жара стояла ужасная. А вместо привычной Айи на зов девочки пришла какая-то совсем незнакомая 
            служанка.
        </div>
        <img src="'''+ path +'''">
    </body>
</html>''', 200, {
    'X-Vector': 'It is me',
    'X-Teapot': 'Tea cup',
    'Content-Language': 'ru-RU'
    }
