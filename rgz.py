from flask import Blueprint, render_template, request, session, current_app
from os import path
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

rgz = Blueprint('rgz', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'maria_byzova_knowledge_base',
            user = 'maria_byzova_knowledge_base',
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


@rgz.route('/rgz/')
def main():
    return render_template('rgz/rgz.html')
