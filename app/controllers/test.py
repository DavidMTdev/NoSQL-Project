  
from flask import Blueprint, request, jsonify, redirect, url_for
from app.settings.database import db

test = Blueprint('test', __name__, url_prefix='/api/test')

@test.route("/")
def getHome():
    print(db.list_collection_names())
    print(db.user.find_one())
    return "Hello World"
