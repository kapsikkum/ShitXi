import io
import os
import sqlite3
import sys
from datetime import date, datetime, timedelta

from flask import (Flask, Response, flash, jsonify, redirect, render_template,
                   render_template_string, request, send_file,
                   send_from_directory, url_for)

from shit import database, utils

app = Flask(__name__,
			static_url_path='',
			static_folder='static/',
			template_folder='templates/')
app.config['SECRET_KEY'] = os.urandom(12)


@app.route("/")
def index():
	return render_template("index.html", pastes=database.get_latest())


@app.route("/archive")
def archive():
	return render_template("archive.html", pastes=database.get_latest(limit=50))


@app.route("/post", methods=['POST'])
def post():
	paste_title = request.form.get('paste_name')
	paste_content = request.form.get('paste_code')
	if paste_title is None and paste_content is None or paste_title == "" and paste_content == "":
		return redirect("/")
	else:
		if sys.getsizeof(paste_content) > 1024000:
			return redirect("/")
		if paste_title == "":
			paste_title = "Untitled"
		link = database.write_paste_data(paste_title, paste_content, request.remote_addr)
		return redirect(f"/{link}")


@app.route("/raw/<paste_id>")
def get_raw_paste(paste_id):
	paste_data = database.read_paste(paste_id)
	if paste_data is not None:
		return str(utils.build_raw(paste_data.content))
	else:
		return send_from_directory("templates/", "404.html"), 404


@app.route("/dl/<paste_id>")
def download_paste(paste_id):
	paste_data = database.read_paste(paste_id)
	if paste_data is not None:
		text = io.BytesIO()
		text.write(paste_data.content.encode('utf-8'))
		text.seek(0)
		if not paste_data.title == "Untitled":
			paste_title = paste_data.title
		else:
			paste_title = paste_data.code
		return send_file(
			text,
			as_attachment=True,
			attachment_filename=f'{paste_title}.txt',
			mimetype='text/plain'
		)
	else:
		return send_from_directory("templates/", "404.html"), 404


@app.route("/<paste_id>")
def get_paste(paste_id):
	paste_data = database.read_paste(paste_id)
	if paste_data is not None:
		database.increase_views(paste_id, paste_data.views)
		return render_template("paste.html", paste=paste_data, pastes=database.get_latest())
	else:
		return send_from_directory("templates/", "404.html"), 404


@app.errorhandler(404)
def error404(e):
	return send_from_directory("templates/", "404.html"), 404


database.init_db()
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=42069)
