import os
import flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask import jsonify


load_dotenv()

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["MONGO_URI"] = os.environ.get('MONGODB_URL')
mongo = PyMongo(app)


@app.route("/", methods=["GET"])
def hello_world():
    return jsonify(
        message="Hello World!"
    )


if (__name__ == "__main__"):
    app.run()
