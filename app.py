import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET"])
def hello_world():
    return "Hello world!"

if (__name__ == "__main__"):
    app.run()