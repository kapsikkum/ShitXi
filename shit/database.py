import sqlite3
from collections import namedtuple
from datetime import datetime

from shit import utils


def connect_to_db():
	conn = sqlite3.connect('database.db', timeout=300)
	c = conn.cursor()
	return conn, c


def init_db():
	conn, c = connect_to_db()
	c.execute('CREATE TABLE IF NOT EXISTS Pastes (id TEXT PRIMARY KEY, timestamp REAL, creator_ip TEXT, title TEXT, data TEXT, views INTEGER);')
	c.execute("CREATE INDEX IF NOT EXISTS Pastes_Index ON Pastes(id);")
	conn.close()


def write_paste_data(paste_title, paste_content, creator_ip):
	conn, c = connect_to_db()
	while True:
		new_id = utils.random_id()
		try:
			c.execute(f'SELECT id FROM Pastes WHERE id="{new_id}"').fetchall()[0][0]
		except:
			break
		else:
			continue
	c.execute(
		"INSERT INTO Pastes VALUES (?, ?, ?, ?, ?, ?)", (new_id, datetime.timestamp(datetime.now()), creator_ip, paste_title, paste_content, 1))
	conn.commit()
	conn.close()
	return new_id


def read_paste(paste_id):
	conn, c = connect_to_db()
	paste_data = c.execute(f'SELECT id, timestamp, creator_ip, title, data, views FROM Pastes WHERE id="{paste_id}"').fetchall()
	conn.close()
	try:
		paste_data[0]
	except:
		return None
	else:
		paste = paste_data[0]
		d = {
			"code": paste[0],
			"timestamp": paste[1],
			"creator_ip": paste[2],
			"title": paste[3],
			"content": paste[4],
			"views": paste[5],
			"human_time": utils.human_time(paste[1], since=False),
			"lines": paste[4].splitlines(),
			"size": utils.get_string_size(paste[4])
		}
		return namedtuple('Paste', sorted(d.keys()))(**d)


def get_latest(limit=10):
	conn, c = connect_to_db()
	pastes = c.execute('SELECT * FROM Pastes ORDER BY timestamp DESC LIMIT ?', (limit,)).fetchall()
	conn.close()
	paste_list = list()
	for paste in pastes:
		d = {
			"code": paste[0],
			"timestamp": paste[1],
			"creator_ip": paste[2],
			"title": paste[3],
			"content": paste[4],
			"views": paste[5],
			"human_time": utils.human_time(paste[1])
		}
		paste_list.append(namedtuple('Paste', sorted(d.keys()))(**d))
	return paste_list


def increase_views(paste_id, views):
	conn, c = connect_to_db()
	c.execute('UPDATE Pastes SET views=? WHERE id=?', (views + 1, paste_id))
	conn.commit()
	conn.close()