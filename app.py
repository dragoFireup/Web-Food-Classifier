from fastai import *
from fastai.vision import *

from flask import Flask, render_template, request, flash, redirect, jsonify

from werkzeug.utils import secure_filename
import os

from io import BytesIO

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["SECRET_KEY"] = "some_key"

def allowed_file(filename):
	return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods = ["GET"])
def home():
	if request.method == "GET":
		return render_template("index.html")

@app.route('/classify', methods=["POST"])
def classify():
	if request.method == "POST":

		print(request.files)

		if "file" not in request.files:
			return jsonify('No File Part')

		file = request.files["file"]
		print(file)

		if file.filename == "":
			return jsonify('No Selected file')

		if file and allowed_file(file.filename):
			image_bytes = file.read()
			image = open_image(BytesIO(image_bytes))

			clas, idx, prob = model.predict(image)

			prob = prob.tolist()

			val = []

			for i in range(len(prob)):
				val.append([model.data.classes[i], prob[i]])

			val = sorted(val, reverse=True, key=lambda x: x[1])
			result = []
			for i in range(3):
				result.append({'name': val[i][0].replace('_', ' ').title(), 'prob': round(val[i][1], 4)*100})

			return jsonify(result)


pathToModel = os.getcwd() + "\\weights"

model = load_learner(Path(pathToModel), 'model-unfreeze.pkl')

if __name__ == "__main__":
	app.run("localhost", port=80, debug=True)