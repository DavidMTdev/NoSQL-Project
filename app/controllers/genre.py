from flask import Blueprint, request, jsonify, redirect, url_for
from app.settings.database import db

genre = Blueprint('genre', __name__, url_prefix='/api/genre')

# Réccupérer par id
#lien : http://127.0.0.1:5000/api/genre/14
@genre.route("/<id>", methods=['GET'])
def getGenre(id):
    #recuperation du genre avec un find_one grace a son id
    genre = db.genres.find_one({"id": int(id)}, {"_id": 0})

    return jsonify(genre)

# Réccupérer tout les genres
#http://127.0.0.1:5000/api/genre/all
@genre.route("/all", methods=['GET'])
def getGenres():
    #recuperation de genre avec un find
    genres = db.genres.find({}, {"_id": 0}).sort("name")

    #permet d'afficher en json
    data = {
        "results": [],
        "count": 0
    }
    for genre in genres:
        #Ajoute genre a la liste result dans data
        data["results"].append(genre)
        #stocker dans count le nombre de ligne recuperer dans la requete
    data["count"] = genres.count()
#affiche les genre 
    return jsonify(data)

# recuperer par name
# http://127.0.0.1:5000/api/genre?name=Science Fiction
@genre.route("", methods=['GET'])
def getGenreByName():
    #recuperation du nom de categorie
    name = request.args.get('name')
    #find avec le nom de categorie
    genres = db.genres.find({"name": name}, {"_id": 0})
    
    data = {
        "results": [],
        "count": 0
    }

    for genre in genres:
        #Ajoute genre a la liste result dans data
        data["results"].append(genre)
    #stocker dans count le nombre de ligne recuperer dans la requete
    data["count"] = genres.count()

    return jsonify(data)


#methode POST
# http://127.0.0.1:5000/api/genre/create
@genre.route("/create", methods=['POST'])
def postGenre():
    req = request.json
    print(req)
    if req :
        #ajout avec l'insert_one
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
# http://127.0.0.1:5000/api/genre/delete/1
@genre.route("/delete/<id>", methods=['DELETE'])
def postDeleteGenre(id):
    #verifie si il y a l'id
    if db.genres.find_one({"id": int(id)}):
        #si l'id est present alors supprimer
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
