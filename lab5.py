from flask import  render_template, Blueprint, request, redirect, session
lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    name = request.cookies.get('name')

    if name is None:
        name = "Anonymous"
    return render_template('lab5/lab5.html', name=name)
