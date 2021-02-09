from flask import Blueprint, request, jsonify, redirect, url_for
from app.settings.database import db

genre = Blueprint('genre', __name__, url_prefix='/api/genre')

# Réccupérer par id
#lien : http://127.0.0.1:5002/api/genre/14
@genre.route("/<id>", methods=['GET'])
def getGenre(id):
    genre = db.genres.find_one({"id": int(id)}, {"_id": 0})

    return jsonify(genre)

# Réccupérer tout les genres
#http://127.0.0.1:5002/api/genre/all
@genre.route("/all", methods=['GET'])
def getGenres():
    genres = db.genres.find({}, {"_id": 0}).sort("name")

    data = {
        "results": [],
        "count": 0
    }

    for genre in genres:
        data["results"].append(genre)

    data["count"] = genres.count()

    return jsonify(data)

# Réccupérer tout les genres  
# http://127.0.0.1:5002/api/genre?name=Science Fiction
@genre.route("", methods=['GET'])
def getGenreByName():
    name = request.args.get('name')
    genres = db.genres.find({"name": name}, {"_id": 0}).sort("name")

    data = {
        "results": [],
        "count": 0
    }

    for genre in genres:
        data["results"].append(genre)

    data["count"] = genres.count()

    return jsonify(data)


#methode POST
# http://127.0.0.1:5002/api/genre/create
@genre.route("/create", methods=['POST'])
def postGenre():
    req = request.json
    print(req)
    if req :
        db.genres.insert_one(req)

        message = {
            "success" : True,
            "message": "genre was created"
        }
    else :
        message = {
            "success": False,
            "message": "The genre wasn't created"
        }

    return jsonify(message)

#methode DELETE
# http://127.0.0.1:5002/api/genre/delete/1
@genre.route("/delete/<id>", methods=['DELETE'])
def postDeleteGenre(id):
    if db.genres.find_one({"id": int(id)}):
        db.genres.delete_one({"id": int(id)})

        message = {
            "success" : True,
            "message": "genre was deleted"
        }
    else :
        message = {
            "success": False,
            "message": "The genre wasn't deleted"
        }

    return jsonify(message)

