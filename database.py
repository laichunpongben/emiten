#!/usr/bin/python3

import time
import sqlite3

DB_NAME = 'emiten.db'

def create():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    sqls = [
        '''CREATE TABLE IF NOT EXISTS opportunities (datetime text, title text, description text, company text, url text, keyword text)''',
        '''CREATE TABLE IF NOT EXISTS companies (company text, location text)'''
    ]
    for sql in sqls:
        c.execute(sql)
    conn.commit()
    conn.close()

def drop():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    sqls = [
        '''DROP TABLE IF EXISTS opportunities''',
        '''DROP TABLE IF EXISTS companies'''
    ]
    for sql in sqls:
        c.execute(sql)
    conn.commit()
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
