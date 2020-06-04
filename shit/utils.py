import random
import string
import sys
import time
from datetime import datetime, timedelta

import humanize
from dominate import document
from dominate.tags import *


def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


def random_id():
	id = str()
	for x in range(8):
		id += random.choice(string.ascii_lowercase +string.ascii_uppercase + string.digits)
	return id


def human_time(timestamp, since=True):
	return (humanize.naturaltime(time.time() - timestamp) if since else custom_strftime('%b {S}, %Y', datetime.fromtimestamp(timestamp)))


def get_string_size(string):
	return humanize.naturalsize(sys.getsizeof(string))


def build_raw(content):
	return html(head(link(rel="shortcut icon", href="/img/favicon.ico"),), body(pre(content, style="word-wrap: break-word; white-space: pre-wrap;")))
