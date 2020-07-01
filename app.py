from fastai import *
from fastai.vision import *

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')



if __name__ == "__main__":
	app.run('localhost', port=80, debug=True)