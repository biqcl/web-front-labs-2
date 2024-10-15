from flask import  render_template, Blueprint, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')

    if name is None:
        name = "друг"
    if age is None:
        age = "(сколько?)"
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie/')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Mar', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', '#A3CCA3')
    return resp


@lab3.route('/lab3/del_cookie/')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name_color')
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('color')
    resp.delete_cookie('bgcolor')
    resp.delete_cookie('fsize')
    resp.delete_cookie('ffamily')
    return resp


@lab3.route('/lab3/form1/')
def form1():
    errors = {}
   
    user = request.args.get('user')
    
    if user == '':
        errors ['user'] = 'Заполните поле!!!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Сколько вам лет??'

    sex = request.args.get('sex')
    return render_template('/lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order/')
def order():
    return render_template('lab3/order.html')


price = 0

@lab3.route('/lab3/pay/')
def pay():
    global price

    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
        
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/paid/')
def paid():
    global price 
    
    return render_template('lab3/paid.html', price=price)


@lab3.route('/lab3/settings/')
def settings():
    color = request.args.get('color')
    bgcolor = request.args.get('bgcolor')
    fsize = request.args.get('fsize')
    ffamily = request.args.get('ffamily')

    if color:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('color', color)
        return resp
    if bgcolor:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('bgcolor', bgcolor)
        return resp
    if fsize:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('fsize', fsize)
        return resp
    if ffamily:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('ffamily', ffamily)
        return resp
    
    color = request.cookies.get('color')
    bgcolor = request.cookies.get('bgcolor') 
    fsize = request.cookies.get('fsize') 
    ffamily  = request.cookies.get('ffamily')
    resp = make_response(render_template('lab3/settings.html', color=color, bgcolor=bgcolor,fsize=fsize, ffamily=ffamily))
    return resp


@lab3.route('/lab3/form2/')
def form2():
    errors = {}
    pass_name = request.args.get('pass_name')
    if pass_name == '':
        errors['pass_name'] = 'Заполните поле!'

    shelf = request.args.get('shelf')
    bedding = request.args.get('bedding') == 'on'
    luggage = request.args.get('luggage') == 'on'
    
    age = request.args.get('age')
    if age == None:
        errors['age'] = ''
    elif age =='':
        errors['age'] = 'Заполните поле!'
    else:
        age = int(age)
        if age < 1 or age > 120:
            errors['age'] = 'Возраст должен быть от 1 до 120 лет!'

    departure = request.args.get('departure')
    if departure == '':
        errors['departure'] = 'Заполните поле!'

    destination = request.args.get('destination')
    if destination == '':
        errors['destination'] = 'Заполните поле!'

    date = request.args.get('date')
    if date == '':
        errors['date'] = 'Заполните поле!'
    
    insurance = request.args.get('insurance') == 'on'

    if 'age' in errors:
        price = 0
        ticket_type = ''
    else:
        if age >= 18:
            base_price = 1000
            ticket_type = 'Взрослый билет'
        else:
            base_price = 700
            ticket_type = 'Детский билет'

        if shelf in ['lower', 'lower_side']:
            base_price += 100
        if bedding:
            base_price += 75
        if luggage:
            base_price += 250
        if insurance:
            base_price += 150

        price = base_price

    return render_template('lab3/form2.html', errors=errors, pass_name=pass_name, shelf=shelf,
                           bedding=bedding, luggage=luggage, age=age, departure=departure,
                           destination=destination, date=date, insurance=insurance,
                           ticket_type=ticket_type, price=price)


books = [
 {"name": "Стивен Кинг", "bname": "Оно", "price": 864, "genre": "Ужасы"},
 {"name": "Джоан Роулинг", "bname": "Гарри Поттер и философский камень", "price": 1026, "genre": "Фэнтези"},
 {"name": "Джордж Оруэлл", "bname": "1984", "price": 450, "genre": "Антиутопия"},
 {"name": "Джейн Остин", "bname": "Гордость и предубеждение", "price": 234, "genre": "Роман"},
 {"name": "Чарльз Диккенс", "bname": "Повесть о двух городах", "price": 1170, "genre": "Исторический роман"},
 {"name": "Эрнест Хемингуэй", "bname": "И восходит солнце", "price": 207, "genre": "Художественная литература"},
 {"name": "Харпер Ли", "bname": "Убить пересмешника", "price": 474, "genre": "Роман"},
 {"name": "Марк Твен", "bname": "Приключения Гекльберри Финна", "price": 383, "genre": "Роман"},
 {"name": "Фрэнсис Скотт Фицджеральд", "bname": "Великий Гэтсби", "price": 284, "genre": "Художественная проза"},
 {"name": "Уильям Шекспир", "bname": "Гамлет", "price": 374, "genre": "Драма"},
 {"name": "Агата Кристи", "bname": "Убийство в Восточном экспрессе", "price": 431, "genre": "Детектив"},
 {"name": "Дэн Браун", "bname": "Код да Винчи", "price": 1231, "genre": "Триллер"},
 {"name": "Пауло Коэльо", "bname": "Алхимик", "price": 574, "genre": "Драма"},
 {"name": "Сьюзан Коллинз", "bname": "Голодные игры", "price": 556, "genre": "Подростковая литература"},
 {"name": "Джон Грин", "bname": "Виноваты звезды", "price": 665, "genre": "Роман"},
 {"name": "Халид Хоссейни", "bname": "Бегущий за ветром", "price": 759, "genre": "Исторический роман"},
 {"name": "Стиг Ларссон", "bname": "Девушка с татуировкой дракона", "price": 831, "genre": "Криминал"},
 {"name": "Вероника Рот", "bname": "Дивергент", "price": 679, "genre": "Антиутопия"},
 {"name": "Рик Риордан", "bname": "Перси Джексон и Похититель молний", "price": 599, "genre": "Фэнтези"},
 {"name": "Дж. Р. Р. Толкин", "bname": "Хоббит", "price": 2190, "genre": "Фэнтези"}
]

@lab3.route('/lab3/search/')
def search():
    return render_template('lab3/search.html')


@lab3.route('/lab3/result/')
def result():
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)

    filtered_books = [
        book for book in books
        if (min_price is None or book['price'] >= min_price) and
           (max_price is None or book['price'] <= max_price)
    ]
    return render_template('lab3/result.html', books=filtered_books)
