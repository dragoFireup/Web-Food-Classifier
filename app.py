from io import BytesIO
from typing import List

from fastai import *
from fastai.vision import *
from flask import Flask, jsonify, render_template, request

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["SECRET_KEY"] = "some_key"


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def predict(img: bytes) -> List:

    pred_class, pred_idx, pred_probs = model.predict(img)
    pred_probs = pred_probs / sum(pred_probs)
    pred_probs = pred_probs.tolist()

    return [pred_class, pred_idx, pred_probs]


def get_topkaccuracy(pred_probs: List, n: int = 3) -> List[dict]:

    class_probs = []
    class_names = get_classnames()

    for i in range(len(pred_probs)):
        class_probs.append((class_names[i], pred_probs[i]))

    class_probs = sorted(class_probs, reverse=True, key=lambda x: x[1])

    top_k = []
    for class_prob in class_probs[:n]:
        top_k.append({"name": class_prob[0], "prob": round(class_prob[1] * 100, 2)})

    return top_k


def get_classnames() -> List:

    class_names = model.data.classes
    for i in range(len(class_names)):
        class_names[i] = class_names[i].replace("_", " ")
        class_names[i] = class_names[i].title()

    return class_names


@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/classify", methods=["POST"])
def classify():
    if request.method == "POST":

        if "file" not in request.files:
            return "No file selected", 404

        file = request.files["file"]

        if file.filename == "":
            return "No File Selected", 404

        if not allowed_file(file.filename):
            return "Please upload an image of type jpg/jpeg/png", 404

        if file and allowed_file(file.filename):
            image = file.read()
            image_bytes = open_image(BytesIO(image))

            pred_class, pred_idx, pred_probs = predict(image_bytes)

            top_k = get_topkaccuracy(pred_probs)

            return jsonify(top_k)


@app.route("/food_classes", methods=["GET"])
def food_list():
    if request.method == "GET":

        return jsonify(get_classnames())


pathToModel = "./weights"

model = load_learner(Path(pathToModel), "model-unfreeze.pkl")


if __name__ == "__main__":
    app.run(port=80, debug=False, threaded=True)
