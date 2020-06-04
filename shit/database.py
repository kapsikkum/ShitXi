import sqlite3
from collections import namedtuple
from datetime import datetime

from sqlite3worker import Sqlite3Worker

from shit import utils

sql = Sqlite3Worker("database.sqlite")


def init_db():
    conn = sqlite3.connect('database.sqlite', timeout=300)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Pastes (id TEXT PRIMARY KEY, timestamp REAL, title TEXT, data TEXT, views INTEGER);')
    c.execute("CREATE INDEX IF NOT EXISTS Pastes_Index ON Pastes(id);")
    conn.close()


def write_paste_data(paste_title, paste_content):
    new_id = utils.random_id()
    sql.execute("INSERT INTO Pastes VALUES (?, ?, ?, ?, ?)", (new_id, datetime.timestamp(datetime.now()), paste_title, paste_content, 1))
    return new_id


def read_paste(paste_id):
    paste_data = sql.execute('SELECT id, timestamp, title, data, views FROM Pastes WHERE id=?', (paste_id, ))
    try:
        paste_data[0]
    except:
        return None
    else:
        paste = paste_data[0]
        d = {
            "code": paste[0],
            "timestamp": paste[1],
            "title": paste[2],
            "content": paste[3],
            "views": paste[4],
            "human_time": utils.human_time(paste[1], since=False),
            "lines": paste[3].splitlines(),
            "size": utils.get_string_size(paste[3])
        }
        return namedtuple('Paste', sorted(d.keys()))(**d)


def get_latest(limit=10):
    pastes = sql.execute('SELECT * FROM Pastes ORDER BY timestamp DESC LIMIT ?', (limit,))
    paste_list = list()
    for paste in pastes:
        d = {
            "code": paste[0],
            "timestamp": paste[1],
            "title": paste[2],
            "content": paste[3],
            "views": paste[4],
            "human_time": utils.human_time(paste[1])
        }
        paste_list.append(namedtuple('Paste', sorted(d.keys()))(**d))
    return paste_list


def increase_views(paste_id, views):
    sql.execute('UPDATE Pastes SET views=? WHERE id=?', (views + 1, paste_id))
