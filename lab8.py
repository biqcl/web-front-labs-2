from flask import  render_template, Blueprint, request, redirect, session
lab8 = Blueprint('lab8', __name__)


@lab8.route('/la8/')
def lab():
    return render_template('lab8/lab8.html')


