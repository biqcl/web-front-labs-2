from flask import  render_template, Blueprint, request, jsonify
lab7 = Blueprint('lab7', __name__)


@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')


films = [
    {
        "title": "What We Do in the Shadows",
        "title_ru": "Реальные упыри",
        "year": 2014,
        "description": "История жизни Виаго, Дикона и Владислава — трёх соседей и по совместительству бессмертных вампиров, которые всего лишь пытаются выжить в современном мире, где есть арендная плата, фейсконтроль в ночных клубах, губительный солнечный свет и другие неприятности."
    },
    {
        "title": "Le Fabuleux destin d'Amélie Poulain",
        "title_ru": "Амели",
        "year": 2001,
        "description": "Знаете ли вы, что все события, происходящие в нашем мире, даже самые незначительные, взаимосвязаны самым удивительным и чудесным образом?"
    },
    {
        "title": "千と千尋の神隠し",
        "title_ru": "Унесённые призраками",
        "year": 2001,
        "description": "Маленькая Тихиро вместе с мамой и папой переезжают в новый дом. Заблудившись по дороге, они оказываются в странном пустынном городе, где их ждет великолепный пир. Родители с жадностью набрасываются на еду и к ужасу девочки превращаются в свиней, став пленниками злой колдуньи Юбабы, властительницы таинственного мира древних богов и могущественных духов."
    },
    {
        "title": "Mamma Mia!",
        "title_ru": "Мамма Mia!",
        "year": 2008,
        "description": "Софи собирается замуж и мечтает, чтобы церемония прошла по всем правилам. Она хочет пригласить на свадьбу отца, чтобы он провёл её к алтарю, но не знает, кто он, так как мать никогда не рассказывала о нём. Софи находит дневник матери, в котором та описывает отношения с тремя мужчинами. Софи решает отправить приглашения всем троим."
    },
    {
        "title": "Ghostbusters",
        "title_ru": "Охотники за привидениями",
        "year": 2016,
        "description": "Тридцать лет назад охотники за привидениями спасли Нью-Йорк от нашествия призраков, но теперь городу вновь угрожает опасность. Былые герои не могут стать на его защиту, но находятся и другие отважные люди, всю свою жизнь посвятившие изучению паранормальных явлений. Эбби Йейтс объединяется с Эрин Гилберт, пожалуй лучшим специалистом в квантовой физике, и вместе они собирают команду новых охотников за привидениями, в которую принимают отличного инженера Джиллиан Хольцман, сотрудницу метрополитена Пэтти Толан, знающую город как свои пять пальцев, и секретаря — настоящего красавчика Кэвина. Вместе они начинают борьбу с нечистой силой, терроризирующей мегаполис..."
    }
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films) #убрать jsonify
    

@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return 'Такого фильма нет :(', 404 
    return films[id]


@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return 'Такого фильма нет :(', 404 
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return 'Такого фильма нет :(', 404 
    film = request.get_json()
    films[id] = film
    return films[id]



