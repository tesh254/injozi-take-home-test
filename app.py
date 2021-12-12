import os
import flask
import datetime
import re
from dotenv import load_dotenv
from flask import jsonify, request
from flask import json
from flask_mongoengine import MongoEngine
from mongoengine.queryset.transform import update
from schema import User, Profile

# JWT dependencies
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# bcrypt dependencies
from flask_bcrypt import Bcrypt

load_dotenv()

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["MONGODB_SETTINGS"] = {
    'host': os.environ.get('MONGODB_URL'),
    'db': os.environ.get('MONGODB_DB'),
}
db = MongoEngine()
db.init_app(app)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Email validator


def check(email):
    if(not re.fullmatch(regex, email)):
        return False
    return True


@app.route('/api/v1/register', methods=['POST'])
def register():
    request_data = request.get_json()

    # handle error if email and password are provided
    if (request_data['email'] == "" or request_data['password'] == ""):
        return jsonify({"message": "Username and password are required"}), 400

    # check if email is valid
    if (check(request_data['email']) == False):
        return jsonify({"message": "Email is not valid"}), 400

    # check password length
    if (len(request_data['password']) < 6):
        return jsonify({"message": "Password is too short"}), 400

    # check if email is already in use
    existing_user = User.objects(email=request_data['email']).first()

    # handle error if email is already in use
    if existing_user is not None:
        return jsonify({"message": "You have an account login"}), 400

    time = datetime.datetime.now()

    # create new user
    user = User(email=request_data['email'],
                password=bcrypt.generate_password_hash(request_data['password']), created=time, updated=time).save()

    # create new profile
    profile = Profile(id_user=user.id, name=request_data['name'],
                      surname=request_data['surname'], phone=request_data['phone'], created=time, updated=time).save()

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "user": {
            "email": user.email
        },
        "token": access_token}), 201


@app.route('/api/v1/login', methods=['POST'])
def login():
    return jsonify(request.get_json())


@app.route('/api/v1/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify(current_user)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint Not found', 'status': 404})


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request, please try again', 'status': 400})


if (__name__ == "__main__"):
    app.run()
