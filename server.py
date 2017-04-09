from utils import *
from flask import Flask, render_template
from flask import request
from random import randint
from time import time
from humbledb import Mongo, Document

class OPData(Document):
	config_database = "mineria"
	config_collection = "training_data"

class OPPhrase(Document):
	config_database = "mineria"
	config_collection = "phrases"
	phrase = "p"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def form():
	if request.method == "POST":
		op = OPData()
		op["original_phrase"] = request.form["phrase"]
		op["user_phrase"] = request.form["usr_phrase"]

		if len(op["original_phrase"].split()) != len(op["user_phrase"].split()):
			values = {}
			values["error"] = 1
			values["timestamp"] = float(request.form["timestamp"])
			values["phrase"] = op["original_phrase"]

			return render_template("form.html", vs=values)

		op["name"] = request.form["name"]
		op["total_time"] = time() - float(request.form["timestamp"])
		op["avg_time_keystroke"] = op["total_time"] / len(op["user_phrase"])
		op["phrase_len_chars"] = len(op["original_phrase"])
		op["phrase_len_words"] = len(op["original_phrase"].split())
		op["failed_words"] = get_failed_words(op["original_phrase"], op["user_phrase"])
		op["failed_chars"] = get_num_failed_chars(op["original_phrase"], op["user_phrase"])

		with Mongo:
			OPData.insert(op)

		return render_template("result.html")

	if request.method == "GET":
		values = {}
		values["error"] = 0
		values["timestamp"] = time()

		with Mongo:
			rnd_num = randint(0, OPPhrase.count() - 1)
			values["phrase"] = OPPhrase.find()[rnd_num]["phrase"]
			
		return render_template("form.html", vs=values)

@app.route("/load", methods=["GET", "POST"])
def loadPhrases():
	if request.method == "POST":
		op = OPPhrase()
		op["phrase"] = request.form["phrase"]

		with Mongo:
			OPPhrase.insert(op)

		return render_template("phrase_form.html")

	if request.method == "GET":
		return render_template("phrase_form.html")
