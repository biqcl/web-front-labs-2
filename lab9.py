from flask import  render_template, Blueprint
lab9 = Blueprint('lab9', __name__)


@lab9.route('/lab9/')
def lab():
    return render_template('lab9/lab9.html')
