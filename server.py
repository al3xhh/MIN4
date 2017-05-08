# -*- coding: utf-8 -*-

from utils import *
from flask import Flask, render_template, Response
from flask import request
from random import randint
from time import time
from humbledb import Mongo, Document
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
import pickle

class OPData(Document):
	config_database = "mineria"
	config_collection = "training_data"

class OPPhrase(Document):
	config_database = "mineria"
	config_collection = "phrases"

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
		op["failed_apostrophes"] = get_failed_punctuation_marks("'", request.form["apostrophes"], op["user_phrase"])
		op["failed_dots"] = get_failed_punctuation_marks(".", request.form["dots"], op["user_phrase"])
		op["failed_commas"] = get_failed_punctuation_marks(",", request.form["commas"], op["user_phrase"])
		op["failed_question_marks"] = get_failed_punctuation_marks("?", request.form["question_marks"], op["user_phrase"])
		op["failed_exclamation_marks"] = get_failed_punctuation_marks("!", request.form["exclamation_marks"], op["user_phrase"])
		op["shift"] = int(request.form["shift"])
		op["del"] = int(request.form["del"])
		op["caps_lock"] = int(request.form["caps"])
		op["time_by_press"] = float(request.form["time"]) / float(request.form["count"])

		with Mongo:
			OPData.insert(op)

		vs = {}
		features = [op["total_time"], op["phrase_len_words"], op["phrase_len_chars"], op["failed_exclamation_marks"], op["failed_dots"], op["failed_apostrophes"],
					op["del"], op["caps_lock"], op["shift"], op["failed_question_marks"], op["failed_commas"], op["time_by_press"], op["failed_chars"], op["avg_time_keystroke"],
					op["failed_words"]]
		names = ["Alejandro", "Christian"]

		clf = joblib.load('../clf.pkl')
		vs["realName"] = op["name"]
		vs["predictName"] = names[int(clf.predict(features))]

		return render_template("result.html", vs=vs)

	if request.method == "GET":
		values = {}
		values["error"] = 0
		values["shift"] = 0
		values["del"] = 0
		values["caps"] = 0
		values["time"] = 0
		values["count"] = 0
		values["timestamp"] = time()

		with Mongo:
			rnd_num = randint(0, OPPhrase.count() - 1)
			values["phrase"] = OPPhrase.find()[rnd_num]["phrase"]
			values["question_marks"] = OPPhrase.find()[rnd_num]["question_marks"]
			values["exclamation_marks"] = OPPhrase.find()[rnd_num]["exclamation_marks"]
			values["dots"] = OPPhrase.find()[rnd_num]["dots"]
			values["commas"] = OPPhrase.find()[rnd_num]["commas"]
			values["apostrophes"] = OPPhrase.find()[rnd_num]["apostrophes"]

		return render_template("form.html", vs=values)

@app.route("/load", methods=["GET", "POST"])
def loadPhrases():
	if request.method == "POST":
		op = OPPhrase()
		org_phrase = request.form["phrase"]
		op["phrase"] = org_phrase
		op["question_marks"] = find_question_marks(org_phrase)
		op["exclamation_marks"] = find_exclamation_marks(org_phrase)
		op["dots"] = find_punctuation_marks(org_phrase, ".")
		op["commas"] = find_punctuation_marks(org_phrase, ",")
		op["apostrophes"] = find_apostrophe(org_phrase)

		with Mongo:
			OPPhrase.insert(op)

		return render_template("phrase_form.html")

	if request.method == "GET":
		return render_template("phrase_form.html")

@app.route("/list", methods=["GET"])
def list():
	with Mongo:
		ops = OPData.find()
		ss = ""
		delimiter = ";"

		for o in ops:
			try:
				ss += str(o["total_time"])
				ss += delimiter
				ss += str(o["phrase_len_words"])
				ss += delimiter
				ss += str(o["phrase_len_chars"])
				ss += delimiter
				ss += str(o["failed_exclamation_marks"])
				ss += delimiter
				ss += str(o["failed_dots"])
				ss += delimiter
				ss += str(o["failed_apostrophes"])
				ss += delimiter
				ss += str(o["del"])
				ss += delimiter
				ss += str(o["caps_lock"])
				ss += delimiter
				ss += str(o["shift"])
				ss += delimiter
				ss += str(o["failed_question_marks"])
				ss += delimiter
				ss += str(o["failed_commas"])
				ss += delimiter
				ss += str(o["time_by_press"])
				ss += delimiter
				ss += str(o["failed_chars"])
				ss += delimiter
				ss += str(o["avg_time_keystroke"])
				ss += delimiter
				ss += str(o["failed_words"])
				ss += delimiter
				ss += str(o["name"])
				ss += "\n"
			except Exception as e:
				print e

	return Response(ss, mimetype="text/csv", headers={"Content-disposition":"attachment; filename=samples.csv"})
