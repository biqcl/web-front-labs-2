import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from flask import  render_template, Blueprint, request, jsonify, current_app
from datetime import datetime

lab8 = Blueprint('lab8', __name__)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'maria_byzova_orm',
            user = 'maria_byzova_orm',
            password = '1304'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab8.route('/la8/')
def lab():
    return render_template('lab8/lab8.html')



