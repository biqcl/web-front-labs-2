from flask import  render_template, Blueprint, request
lab7 = Blueprint('lab7', __name__)


@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')


