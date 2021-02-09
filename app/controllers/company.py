from pprint import pprint

from flask import Blueprint, request, jsonify, redirect, url_for
from app.settings.database import db

company = Blueprint('company', __name__, url_prefix='/api/company')
companies = db.companies

# http://127.0.0.1:5000/api/company/all?page=1
# page max 1342
@company.route("/all", methods=['GET'])
def getCompanies():
    """   returns [jsonify] : companyJson   """

    # récupération de la page dans les parametres
    page = request.args.get('page')

    # results : toutes les companies, count_total : total des companies, page : la page, 
    # message : si donnée récuperer success sinon false
    companyJson = {
        "results" : [],
        "page" : page,
        "message" : "success"
    }
    
    companie = []
    
    # verification si page n'est pas null et si c'est bien un int
    if page and page.isdigit() :
        # récupération de toutes les companies , paginer par 20, par rapport à la page 
        companie = companies.find({}, {"_id" : 0}).limit(20).skip(20 * (int(page) - 1))
        companyJson["count_total"] = companie.count()
        companyJson["page"] = page

    # on ajoute les companies dans companyJson["results"]
    for company in companie : 
        companyJson["results"].append(company)

    # dans le json on rajoute le nombre de companies récuperer sur la page
    companyJson["count"] = len(companyJson["results"])

    # si il n'y a pas de donnée on renvoie un message d'erreur
    if companyJson["count"] == 0 :
        companyJson["message"] = "No data could be retrieved"

    return jsonify(companyJson)


# http://127.0.0.1:5000/api/company/filter?id=2
# http://127.0.0.1:5000/api/company/filter?name=Walt%20Disney%20Pictures
@company.route("/filter", methods=['GET'])
def getCompanie():
    """   returns [jsonify] : companyJson   """

    # on recupere soit l'id soit le name
    id = request.args.get('id')
    name = request.args.get('name')

    companie = []

    # si y'a un name on un id alors on fait une query 
    if name and not name.isdigit():
        companie = companies.find({"name": name}, {"_id" : 0})
    elif id and id.isdigit() : 
        companie = companies.find({"id": int(id)}, {"_id" : 0})

    companyJson = {
        "results" : [],
        "message" : "success",
        "count" : 1
    }

    # on ajoute dans companyJson["results"] le resultat de la query
    for company in companie : 
        companyJson["results"].append(company)

    # si liste companyJson["results"] est vide alors message erreur
    if not companyJson["results"] :
        companyJson["message"] = "No data could be retrieved"
        companyJson["count"] = 0

    return jsonify(companyJson)


# http://127.0.0.1:5000/api/company/origin?country=US&page=1
@company.route("/origin", methods=['GET'])
def getCompanieByOrigin():
    """   returns [jsonify] : companyJson   """

    page = request.args.get('page')
    country = request.args.get('country')

    companyJson = {
        "results" : [],
        "message" : "success",
    }

    companie = []
    
    # si page et country on fait la query
    if page and country and page.isdigit() :
        companie = companies.find({"origin_country": country}, {"_id" : 0}).limit(20).skip(20 * (int(page) - 1))
        companyJson["count_total"] = companie.count()
        companyJson["page"] = page

    # on ajoute dans companyJson["results"] le resultat de la query
    for company in companie : 
        companyJson["results"].append(company)

    # dans le json on rajoute le nombre de companies récuperer sur la page
    companyJson["count"] = len(companyJson["results"])

    # si liste companyJson["results"] vide message erreur
    if not companyJson["results"] :
        companyJson["message"] = "No data could be retrieved"

    return jsonify(companyJson)

# http://127.0.0.1:5000/api/company/create
@company.route("/create",  methods=['POST'])
def postCreateCompany():
    req = request.json
    if req :
        db.companies.insert_one(req)

        message = {
            "success": True,
            "message": "company was created"
        }
    else :
        message = {
            "success": False,
            "message": "The company wasn't created"
        }

    return jsonify(message)


# http://127.0.0.1:5000/api/company/delete/100000
@company.route("/delete/<id>",  methods=['DELETE'])
def postDeleteCompany(id):
    if db.companies.find_one({"id": int(id)}):
        db.companies.delete_one({"id": int(id)})

        message = {
            "success": True,
            "message": "company was deleted"
        }
    else :
        message = {
            "success": False,
            "message": "The company wasn't deleted"
        }

    return jsonify(message)