from flask import  render_template, Blueprint, request, redirect, url_for, make_response
lab9 = Blueprint('lab9', __name__)


@lab9.route('/lab9/', methods=['GET', 'POST'])
def lab():
    last_congrats = request.cookies.get('last_congrats')
    last_image = request.cookies.get('last_image')

    if last_congrats and last_image:
        return render_template('lab9/congratulations.html', congrats=last_congrats, image=last_image)

    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('lab9.age', name=name))
    return render_template('lab9/lab9.html')


@lab9.route('/lab9/age/', methods=['GET', 'POST'])
def age():
    name = request.args.get('name')
    if request.method == 'POST':
        age = request.form['age']
        return redirect(url_for('lab9.gender', name=name, age=age))
    return render_template('lab9/age.html', name=name)


@lab9.route('/lab9/gender/', methods=['GET', 'POST'])
def gender():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form['gender']
        return redirect(url_for('lab9.preference', name=name, age=age, gender=gender))
    return render_template('lab9/gender.html', name=name, age=age)


@lab9.route('/lab9/preference/', methods=['GET', 'POST'])
def preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    if request.method == 'POST':
        preference = request.form['preference']
        return redirect(url_for('lab9.final_question', name=name, age=age, gender=gender, preference=preference))
    return render_template('lab9/preference.html', name=name, age=age, gender=gender)


@lab9.route('/lab9/final_question/', methods=['GET', 'POST'])
def final_question():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    if request.method == 'POST':
        final_choice = request.form['final_choice']
        return redirect(url_for('lab9.congratulations', name=name, age=age, gender=gender, preference=preference, final_choice=final_choice))
    return render_template('lab9/final_question.html', name=name, age=age, gender=gender, preference=preference)


@lab9.route('/lab9/congratulations/')
def congratulations():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    final_choice = request.args.get('final_choice')

    if 1 <= age <= 18:
        age_category = "ребенок"
    else:
        age_category = "взрослый"

    if preference == 'что-то вкусное':
        if final_choice == 'сладкое':
            gift = 'сладкий подарок'
            image_child = 'sweet.jpg' 
            image_adult = 'sweet1.jpg' 
        else:
            gift = 'новогодняя корзина'
            image_child = 'food.jpg'  
            image_adult = 'food1.jpg'  
    else:
        if final_choice == 'что-то полезное':
            gift = 'ёлочная игрушка'
            image_child = 'toy.jpg'  
            image_adult = 'toy1.jpg' 
        else:
            gift = 'новогодняя кружка'
            image_child = 'cup.jpg' 
            image_adult = 'cup1.jpg' 

    if age_category == "ребенок":
        image = image_child
    else:
        image = image_adult

    if age_category == "ребенок":
        if gender == 'женский':
            congrats = f"Поздравляю тебя, дорогая {name}, с наступающим Новым годом! Пусть всё, о чём ты мечтаешь, исполнится, а год принесет приятные сюрпризы, удачу, счастье и успех. Вот тебе подарок — {gift}!"
        else:
            congrats = f"Поздравляю тебя, дорогой {name}, с наступающим Новым годом! Пусть всё, о чём ты мечтаешь, исполнится, а год принесет приятные сюрпризы, удачу, счастье и успех. Вот тебе подарок — {gift}!"
    else:
        if gender == 'женский':
            congrats = f"Поздравляю вас, дорогая {name}, с наступающим Новым годом! Пусть весь следующий год будет полон новых побед и достижений, удач и приятных событий. Пусть жизнь будет насыщенной и увлекательной! Вот ваш подарок — {gift}!"
        else:
            congrats = f"Поздравляю вас, дорогой {name}, с наступающим Новым годом! Пусть весь следующий год будет полон новых побед и достижений, удач и приятных событий. Пусть жизнь будет насыщенной и увлекательной! Вот ваш подарок — {gift}!"

    response = make_response(render_template('lab9/congratulations.html', congrats=congrats, image=image))
    response.set_cookie('last_congrats', congrats)
    response.set_cookie('last_image', image)
    return response


@lab9.route('/lab9/reset/', methods=['POST'])
def reset():
    response = make_response(redirect(url_for('lab9.lab')))
    response.delete_cookie('last_congrats')
    response.delete_cookie('last_image')
    return response
