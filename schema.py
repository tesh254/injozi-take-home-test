from typing_extensions import Required
from flask_mongoengine import MongoEngine
from mongoengine.queryset.transform import update

db = MongoEngine()


class User(db.Document):
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    created = db.DateTimeField(default=db.datetime.now, required=True)
    updated = db.DateTimeField(default=db.datetime.now, required=True)


class Profile(db.Document):
    id_user = db.ReferenceField(User, required=True)
    name = db.StringField()
    surname = db.StringField()
    phone = db.StringField()
    created = db.DateTimeField(default=db.datetime.now, required=True)
    updated = db.DateTimeField(default=db.datetime.now, required=True)
