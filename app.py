import os
import flask
from dotenv import load_dotenv
from flask import jsonify
from flask_mongoengine import MongoEngine

load_dotenv()

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["MONGODB_SETTINGS"] = {
    'host': os.environ.get('MONGODB_URL'),
    'db': os.environ.get('MONGODB_DB'),
}
app.config['APPLICATION_ROOT'] = '/v1'
db = MongoEngine()
db.init_app(app)


@app.route("/", methods=["GET"])
def hello_world():
    return jsonify(
        message="Hello World!"
    )


if (__name__ == "__main__"):
    app.run()
