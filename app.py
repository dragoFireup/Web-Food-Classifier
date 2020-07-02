from fastai import *
from fastai.vision import *

from flask import Flask, render_template, request, flash, redirect

from werkzeug.utils import secure_filename
import os

from io import BytesIO

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["SECRET_KEY"] = "some_key"

def allowed_file(filename):
	return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods = ["GET", "POST"])
def home():
	
	if request.method == "GET":
		return render_template("index.html")

	elif request.method == "POST":

		print(request.files)

		if "file" not in request.files:
			flash("No File Part")
			return redirect(request.url)

		file = request.files["file"]
		print(file)

		if file.filename == "":
			flash("No Selected file")
			return redirect(request.url)

		if file and allowed_file(file.filename):
			image_bytes = file.read()
			image = open_image(BytesIO(image_bytes))

			x = model.predict(image)
			

			return redirect(request.url)


pathToModel = os.getcwd() + "\\weights"

model = load_learner(Path(pathToModel), 'model-unfreeze.pkl')

if __name__ == "__main__":
	app.run("localhost", port=80, debug=True)