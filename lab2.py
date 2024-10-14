from flask import  url_for, redirect, render_template, request, Blueprint
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слешем'


flower_list = [
    {'name': 'Анемон', 'price': 100},
    {'name': 'Ранункулюс', 'price': 150},
    {'name': 'Пион', 'price': 200},
    {'name': 'Мак', 'price': 120},
    {'name': 'Фрезия', 'price': 130}
]

@lab2.route('/lab2/flowers/')
def all_flowers():
    flowers=flower_list
    length = len(flower_list)
    return render_template('lab2/flowers.html', flower_list=flowers, length=length)


@lab2.route('/lab2/flowers/<int:flower_id>/')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return 'Такого цветка ещё нет', 404
    else:
        flower = flower_list[flower_id]
    return render_template('lab2/flower_detail.html', flower=flower, flower_id=flower_id)    
    

# @lab2.route('/lab2/add_flower/<name>/<int:price>/')
# def add_flower(name, price):
#     flower_list.lab2end({'name': name, 'price': price})
#     total_flowers = len(flower_list)
#     return render_template('add_flower.html', name=name, price=price, total_flowers=total_flowers)


@lab2.route('/lab2/add_flower/')
def add_flower():
    name = request.args.get('name')
    price = request.args.get('price')
    
    if name and price:  
        flower_list.append({'name': name, 'price': int(price)})
        flower_id = len(flower_list) - 1  
        return redirect(url_for('lab2.flowers', flower_id=flower_id))    
    return "Задайте имя цветка и его цену!!!", 400


# @lab2.route('/lab2/add_flower/') 
# def no_flower_error():
#     return 'Задайте имя цветка и его цену!!!', 400


@lab2.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()  
    return redirect(url_for('lab2.all_flowers'))    
#     return'''
# <!doctype html>
# <html>
#     <head>
#         <link rel="stylesheet" type="text/css" href="''' + style + '''">
#     </head>
#     <body>
#         <h1>Список цветов успешно очищен!</h1>
#         <p><a href="/lab2/flowers/">Вернуться к списку цветов</a></p>
#     </body>
# </html>
# '''


@lab2.route('/lab2/delete_flower/<int:flower_id>/')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        return 'такого цветка и не было', 404  
    else:
        del flower_list[flower_id] 
        return redirect(url_for('lab2.all_flowers'))


@lab2.route('/lab2/example/')
def example():
    name = 'Бызова Мария'
    lab_number = '2'    
    group = 'ФБИ-22'
    course_number = '3'
    fruits = [
        {'name': 'яблоки', 'price': 100}, 
        {'name': 'груши', 'price': 120},
        {'name': 'мандарины', 'price': 96},
        {'name': 'манго', 'price': 315},
        {'name': 'персики', 'price': 140},
    ]
    return render_template('lab2/example.html', name=name, lab_number=lab_number, 
                           group=group, course_number=course_number, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters/')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('lab2/filter.html', phrase=phrase)  


@lab2.route('/lab2/calc/<int:a>/<int:b>/')
def calculation(a, b):
    num_1 = a
    num_2 = b
    add = a + b
    sub = a - b
    multi = a * b
    divis = a / b if b != 0 else "Делить на ноль нельзя"
    exp = a ** b

    return render_template('lab2/calc.html',
                           a=a,
                           b=b,
                           add=add,
                           sub=sub,
                           multi=multi,
                           divis=divis,
                           exp=exp)


@lab2.route('/lab2/calc/')
def def_calc():
    return redirect(url_for('lab2/lab2.calculation', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>/')
def single_number(a):
    return redirect(url_for('lab2/lab2.calculation', a=a, b=1))

books = [
    {"author": "Агата Кристи", "title": "Убийство в восточном экспрессе", "genre": "Детектив", "pages": 320},
    {"author": "Оскар Уайлд", "title": "Портрет Дориана Грея", "genre": "Роман", "pages": 323},
    {"author": "Стивен Кинг", "title": "11/22/63", "genre": "Фантастика", "pages": 928},
    {"author": "Рэй Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Научная фантастика", "pages": 174},
    {"author": "Олдос Хаксли", "title": "О дивный новый мир", "genre": "Антиутопия", "pages": 352},
    {"author": "Акутагава Рюноске", "title": "Ворота расёмон", "genre": "Фикшн", "pages": 576},
    {"author": "Уильям Голдинг", "title": "Повилитель мух", "genre": "Проза", "pages": 318},
    {"author": "Сартр", "title": "Тошнота", "genre": "Роман", "pages": 332},
    {"author": "Фрэнсис Бёрнетт", "title": "Таинственный сад", "genre": "Зарубежная классика", "pages": 272},
    {"author": "Франц Кафка", "title": "Превращение", "genre": "Новелла", "pages": 416}
]


@lab2.route('/lab2/books/')
def book():
    return render_template('lab2/books.html', books=books)

dogs = [
    {
        "name": "Мальтипу",
        "image": "dog1.jpg",
        "description": "Мальтипу – дизайнерская собака, которую вывели осознанно, путем скрещивания двух пород собак: Мальтезе (Мальтийской Болонки) и Той Пуделя."
    },
    {
        "name": "Такса",
        "image": "dog2.jpg",
        "description": "Та́кса — порода южно-немецких норных охотничьих собак. Существует несколько разновидностей такс, отличающихся размерами и весом — стандартные, миниатюрные и кроличьи. Также такс разделяют по шёрстному покрову на гладкошерстных, длинношёрстных и жесткошёрстных. Таксы имеют множество окрасов."
    },
    {
        "name": "Сиба-ину",
        "image": "dog3.jpg",
        "description": "Си́ба-и́ну, или сиба-кэн, — порода охотничьих собак, выведенная на японском острове Хонсю, самая мелкая из шести пород исконно японского происхождения. В 1936 году объявлена национальным достоянием Японии, где основное поголовье этих собак находится в деревнях. Сиба относится к древним породам."
    },
    {
        "name": "Цвергшнауцер",
        "image": "dog4.avif",
        "description": "Цвергшна́уцер, миниатюрный шнауцер, карликовый шнауцер, до 1895 года в Германии и до 1926 года в США также жесткошёрстный пинчер — самая маленькая по размеру служебная собака в мире. Цвергшнауцер является самой маленькой породой из группы шнауцеров."
    },
    {
        "name": "Пудель",
        "image": "dog5.jpg",
        "description": "Пудель — порода, которая на данный момент относится преимущественно к группе декоративных собак. Изначально пудель являлся рабочей собакой, в частности использовался на охоте. Пудель занимает второе место в рейтинге самых умных пород, составленном доктором Стенли Кореном, после бордер-колли."
    }
]


@lab2.route('/lab2/dogs/')
def dogs_woof():
    return render_template('lab2/dogs.html', dogs=dogs)  