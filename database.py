#!/usr/bin/python3

import time
import sqlite3

DB_NAME = 'emiten.db'

def create():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE opportunities (datetime text, title text, description text, company text, url text, keyword text)''')
    conn.commit()
    conn.close()

def drop():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('''DROP TABLE opportunities''')
        conn.commit()
    except sqlite3.OperationalError as e:
        print(e)
    conn.close()

def save(**kwargs):
    title = kwargs.get('title', '')
    description = kwargs.get('description', '')
    company = kwargs.get('company', '')
    url = kwargs.get('url', '')
    keyword = kwargs.get('keyword', '')
    time_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    sql = "INSERT INTO opportunities VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
           time_, title, description, company, url, keyword)
    c.execute(sql)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    drop()
    create()
