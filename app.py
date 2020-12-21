from flask import Flask, render_template
import datetime
from datetime import datetime as dt
import pymongo
import random
import os

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
# MongoDB
cluster = pymongo.MongoClient(os.getenv('MONGO_DB_URL'))
db = cluster["stats"]["stats"]


def fetch(bot_name, delta):
	# Get bot's data from last range
	bot_data = db.find({"bot_name": bot_name})
	bot_commands = db.distinct("command", {"bot_name": bot_name})
	today = datetime.date.today()
	if delta:
		start_delta = datetime.timedelta(days=delta)
		last_range = today - start_delta
		bot_data_list = [d for d in bot_data if dt.strptime(d['date'], '%Y-%m-%d').date() >= last_range ]
	else:
		bot_data_list = [d for d in bot_data]

	# Get sorted dates as labels
	dates = set(d['date'] for d in bot_data_list)
	dates_objects = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in dates]
	dates_objects.sort()
	labels = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates_objects]

	# Pack needed data in datasets for Chart.js
	datasets = []
	for command in bot_commands:
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)

		command_data = {
			"label": command,
			"backgroundColor": f'rgb({r}, {g}, {b})',
			"borderColor": f'rgb({r}, {g}, {b})',
			"data": []
		}

		for label in labels:
			counter = 0
			for d in bot_data_list:
				if d['date'] == label and d['command'] == command:
					counter += 1
			command_data['data'].append(counter)

		datasets.append(command_data)

	lang_data = {
		"labels": [],
		"datasets": [{
			"data": [],
			"backgroundColor": []
		}]
	}
	for d in bot_data_list:
		if "lang" in d.keys() and d["lang"].upper() in lang_data["labels"]:
			ind = lang_data["labels"].index(d['lang'].upper())
			lang_data["datasets"][0]["data"][ind] += 1
		elif "lang" in d.keys():
			lang_data["labels"].append(d["lang"].upper())
			r = random.randint(0, 255)
			g = random.randint(0, 255)
			b = random.randint(0, 255)
			lang_data["datasets"][0]["backgroundColor"].append(f'rgb({r}, {g}, {b})')
			lang_data["datasets"][0]["data"].append(1)

	return dict({"labels": labels, "datasets": datasets, "lang_data": lang_data})


@ app.route("/")
def index():
	bot_list = db.distinct("bot_name")
	return render_template("index.html", bot_list=bot_list)


@ app.route("/<string:bot_name>")
def bot(bot_name):
	bot_data = db.find({"bot_name": bot_name})
	bot_data_list = [d for d in bot_data]
	return str(bot_data_list)


@ app.route("/<string:bot_name>/<int:delta>")
def bot_week(bot_name, delta):
	return fetch(bot_name, delta)


if __name__ == '__main__':
	app.run(debug=False)
