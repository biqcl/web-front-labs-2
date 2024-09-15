from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/web")
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

@app.route("/author")
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
               <a href="/web">web</a>
           </body>
        </html>"""

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    return '''
<!doctype html>>
<html>
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

@app.route("/info")
def info():
   return redirect("/author")

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
