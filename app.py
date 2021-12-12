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
app.config["JWT_SECRET_KEY"] = os.environ.get('SECRET_KEY')  # Change this!
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
        return jsonify({"message": "email and password are required"}), 400

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
    Profile(id_user=user.id, name=request_data['name'],
            surname=request_data['surname'], phone=request_data['phone'], created=time, updated=time).save()

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "user": {
            "email": user.email
        },
        "token": access_token}), 201


@app.route('/api/v1/login', methods=['POST'])
def login():
    request_data = request.get_json()

    # check if email and password were provided
    if (request_data['email'] == '' and request_data['password'] == ''):
        return jsonify({"message": "email and password are required"}), 400

    # check if email is valid
    if (check(request_data['email']) == False):
        return jsonify({"message": "Email is not valid"}), 400

    # check if password is long enough
    if (len(request_data['password']) < 6):
        return jsonify({"message": "Password is too short"}), 400

    # get user by email
    existing_user = User.objects(email=request_data['email']).first()

    if (existing_user is None):
        return jsonify({"message": "Account not found"}), 404

    # check if password to account is correct
    pass_hash_result = bcrypt.check_password_hash(
        existing_user.password, request_data['password'])

    if (pass_hash_result is False):
        return jsonify({'message': 'Email or password is incorrect'}), 401

    # generate access token from id
    access_token = create_access_token(identity=str(existing_user.id))

    return jsonify(access_token=access_token, message='Log in successful'), 200


@app.route('/api/v1/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()

    existing_user = User.objects(id=current_user).first()

    if existing_user is None:
        return jsonify(message='Account does not exist'), 401

    existing_profile = Profile.objects(id_user=existing_user).first()

    return jsonify({
        "name": existing_profile['name'],
        'surname': existing_profile['surname'],
        'email': existing_user['email'],
        'phone': existing_profile['phone']
    }), 200

@app.route('/api/v1/profiles', methods=['GET'])
def list_profiles():
    profiles = Profile.objects().all_fields()

    return jsonify(profiles=profiles)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint Not found', 'status': 404}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request, please try again', 'status': 400}), 400


@app.errorhandler(500)
def internal_server_error(error):
    print(error)
    return jsonify({'error': 'Internal Server Error', 'status': 500}), 500


if (__name__ == "__main__"):
    app.run()
