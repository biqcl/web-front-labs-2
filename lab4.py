from flask import  render_template, Blueprint, request, redirect
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form/')
def div_form():
    return render_template('/lab4/div-form.html')


@lab4.route('/lab4/div/', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('/lab4/div.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('/lab4/div.html', error='На ноль делить нельзя!')

    result = x1 / x2
    return render_template('/lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form/')
def sum_form():
    return render_template('/lab4/sum-form.html')


@lab4.route('/lab4/sum/', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' and x2 == '':
        return render_template('/lab4/sum.html', error='Хотя бы одно поле должно быть заполнено!')
    
    if x1 == '':
        x1 = 0
    if x2 == '':
        x2 = 0

    x1 = int(x1)
    x2 = int(x2)

    result = x1 + x2
    return render_template('/lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/multi-form/')
def multiply_form():
    return render_template('/lab4/multi-form.html')


@lab4.route('/lab4/multi/', methods = ['POST'])
def multi():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' and x2 == '':
        return render_template('/lab4/multi.html', error='Хотя бы одно поле должно быть заполнено!')
    
    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1

    x1 = int(x1)
    x2 = int(x2)

    result = x1 * x2
    return render_template('/lab4/multi.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form/')
def sub_form():
    return render_template('/lab4/sub-form.html')


@lab4.route('/lab4/sub/', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('/lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)

    result = x1 - x2
    return render_template('/lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/exp-form/')
def exp_form():
    return render_template('/lab4/exp-form.html')


@lab4.route('/lab4/exp/', methods = ['POST'])
def exp():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('/lab4/exp.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)

    result = x1 ** x2
    return render_template('/lab4/exp.html', x1=x1, x2=x2, result=result)


tree_count = 0

@lab4.route('/lab4/tree/', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('/lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        tree_count += 1
    
    return redirect ('/lab4/tree')


users = [
    {'login': 'Alex', 'password': '123'},
    {'login': 'Masha', 'password': '1304'},
    {'login': 'Ksusha', 'password': '1810'},
    {'login': 'Bob', 'password': '555'}
]

@lab4.route('/lab4/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/lab4/login.html', authorized=False)
    
    login = request.form.get('login')
    password = request.form.get('password')
    for user in users:
        if login == user['login'] and password == user['password']:
            return render_template('/lab4/login.html', error='Успешная авторизация', authorized=True, login=login)
    
    error = 'неверные логин и/или пароль'
    return render_template('/lab4/login.html', error=error, authorized=False)

