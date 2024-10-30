from flask import  render_template, Blueprint, request, redirect, session
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
    {'login': 'alex', 'password': '123', 'name': 'Алекс Тёрнер', 'gender': 'мужской'},
    {'login': 'bob', 'password': '555', 'name': 'Роберт Дилан', 'gender': 'мужской'},
    {'login': 'mar', 'password': '1304', 'name': 'Мария Бызова', 'gender': 'женский'},
    {'login': 'ksu', 'password': '1810', 'name': 'Ксения Бызова', 'gender': 'женский'}
]

@lab4.route('/lab4/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' and 'gender' in session:
            authorized = True
            name = session['name']
            gender = session['gender']
        else:
            authorized=False
            name = ''
            gender = ''
        return render_template('/lab4/login.html', authorized=authorized, name=name, gender=gender)
    
    login = request.form.get('login')
    if login == '':
        error = 'Не введён логин'
        return render_template('/lab4/login.html', error=error, authorized=False)

    password = request.form.get('password')
    if password == '':
        error = 'Не введён пароль'
        return render_template('/lab4/login.html', error=error, authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = user['login']
            session['name'] = user['name']
            session['gender'] = user['gender']
            return redirect('/lab4/login/')
    
    error = 'Неверные логин и/или пароль'
    return render_template('/lab4/login.html', error=error, authorized=False, login=login)


@lab4.route('/lab4/logout/', methods = ['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    session.pop('gender', None)
    return redirect('/lab4/login/')


@lab4.route('/lab4/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        name = request.form.get('name')
        gender = request.form.get('gender')

        if not login or not password or not name:
            error = 'Все поля обязательны'
            return render_template('/lab4/register.html', error=error)
            
        for user in users:
            if user['login'] == login:
                error = 'Логин уже занят'
                return render_template('/lab4/register.html', error=error)

        users.append({'login': login, 'password': password, 'name': name, 'gender': gender})
        return redirect('/lab4/login/')

    return render_template('/lab4/register.html')


@lab4.route('/lab4/users/')
def user_list():
    if 'login' not in session:
        return redirect('/lab4/login/')
    
    return render_template('/lab4/user_list.html', users=users, name=session['name'])


@lab4.route('/lab4/delete_user/')
def delete_user():
    if 'login' in session:
        current_login = session['login']

        for user in users:
            if user['login'] == current_login:
                users.remove(user)
                
        logout()
    return redirect('/lab4/login/')


@lab4.route('/lab4/edit_user/', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login/')
    
    for user in users:
        if user['login'] == session['login']:
            current_user = user

    if request.method == 'POST':
        current_user['name'] = request.form.get('name')
        current_user['password'] = request.form.get('password')
        return redirect('/lab4/users/')

    return render_template('/lab4/edit_user.html', user=current_user)


@lab4.route('/lab4/fridge-form/')
def fridge_form():
    return render_template('/lab4/fridge-form.html')


@lab4.route('/lab4/fridge/', methods=['POST'])
def fridge():
    temperature = request.form.get('temperature')

    if temperature == '':
        return render_template('/lab4/fridge.html', error='Ошибка: не задана температура')

    temperature = int(temperature)

    if temperature < -12:
        return render_template('/lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    elif temperature > -1:
        return render_template('/lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    else:
        return render_template('/lab4/fridge.html', temperature=temperature)


@lab4.route('/lab4/seed-form/')
def seed_form():
    return render_template('/lab4/seed-form.html')


@lab4.route('/lab4/seed', methods=['POST'])
def seed():
    seed_type = request.form.get('seed')
    weight = request.form.get('weight')

    if weight == '':
        return render_template('/lab4/seed-form.html', error='Укажите вес!')

    weight = int(weight)

    if weight <= 0:
        return render_template('/lab4/seed-form.html', error='Вес должен быть больше 0!')

    if weight > 500:
        return render_template('/lab4/seed-form.html', error='Такого объёма сейчас нет в наличии :(')

    if seed_type == "ячмень":
        price_per_ton = 12345
    elif seed_type == "овёс":
        price_per_ton = 8522
    elif seed_type == "пшеница":
        price_per_ton = 8722
    else:
        price_per_ton = 14111

    total_cost = price_per_ton * weight

    discount = 0
    if weight > 50:
        discount = total_cost * 0.1
        total_cost -= discount
    return render_template('/lab4/seed.html', seed=seed_type, weight=weight, total_cost=total_cost, discount=discount)
    