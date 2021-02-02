from pprint import pprint

from flask import Blueprint, request, jsonify, redirect, url_for
from app.settings.database import db

movie = Blueprint('movie', __name__, url_prefix='/api/movie')

joinGenres = { 
    "$lookup": {
        "localField": "genres.id",
        "from": "genres",
        "foreignField": "id",
        "as": "genres"
    } 
}
joinCompanies = {
    "$lookup": {
        "localField": 'production_companies.id',
        "from": 'companies',
        "foreignField": 'id',
        "as": 'production_companies'
    }
}
addFields = { 
    "$addFields": {
        "genres": "$genres",            
        "production_companies": "$production_companies"
    } 
}
project = { 
    "$project": {
        "_id": 0,
        "genres._id" : 0,
        "production_companies._id": 0
    }
}

# http://localhost:5000/api/movie/2
@movie.route("/<id>")
def getMovie(id):
    match = { "$match": { "id": int(id) }}
    movie = db.movies.aggregate([match, joinGenres, joinCompanies, addFields, project])

    return jsonify(list(movie)[0])

# http://localhost:5000/api/movie/all
@movie.route("/all")
def getMovies():
    page = request.args.get('page')

    limit = {"$limit": 20}
    skip = {"$skip": 20 * (int(page) - 1)}
    movies = db.movies.aggregate([joinGenres, joinCompanies, addFields, project, skip, limit])
    
    data = {
        "results": [],
        "page" : page,
        "count": 0
    }
    
    for movie in movies:
        data["results"].append(movie)
    
    data["count"] = len(data["results"])
    
    return jsonify(data)

# http://localhost:5000/api/movie?page=1&title=Star%20Trek
@movie.route("")
def getMovieByTitle():
    page = request.args.get('page')
    title = request.args.get('title')

    match = { "$match": {"title": {"$regex": title}}}
    limit = {"$limit": 20}
    skip = {"$skip": 20 * (int(page) - 1)}
    movies = db.movies.aggregate([match, joinGenres, joinCompanies, addFields, project, skip, limit])
    
    data = {
        "results": [],
        "query": {
            "title": title
        },
        "page" : page,
        "count": 0
    }
    
    for movie in movies: 
        data["results"].append(movie)
        
    data["count"] = len(data["results"])

    return jsonify(data)

# http://127.0.0.1:5000/api/movie/all/notes?page=4
@movie.route("/all/notes")
def getMovieClassedByNote():
    page = request.args.get('page')
    minimum = request.args.get('min')
    maximum = request.args.get('max')

    limit = {"$limit": 20}
    skip = {"$skip": 20 * (int(page) - 1)}
    sort = {"$sort": {"vote_average": -1}} 

    data = {
        "results": [],
        "query": {
            "min": minimum,
            "max": maximum
        },
        "page" : page,
        "count": 0
    }

    if maximum != None and minimum != None:
        match = { "$match": {"vote_average": {"$gt": int(minimum) , "$lt": int(maximum) }}}
        pprint("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        movies = db.movies.aggregate([match, joinGenres, joinCompanies, addFields, project, skip, limit, sort])
    elif maximum != None:
        match = { "$match": {"vote_average": {"$lt":  int(maximum)}}}

        movies = db.movies.aggregate([match, joinGenres, joinCompanies, addFields, project, skip, limit, sort])
    elif minimum != None:
        match = { "$match": {"vote_average": {"$gt":  int(minimum)}}}
        
        movies = db.movies.aggregate([match, joinGenres, joinCompanies, addFields, project, skip, limit, sort])
    else:
        movies = db.movies.aggregate([joinGenres, joinCompanies, addFields, project, skip, limit, sort])
    
    for movie in movies: 
        data["results"].append(movie)

    data["count"] = len(data["results"])

    return jsonify(data)

# http://127.0.0.1:5000/api/movie/company/2302?page=4
@movie.route("/company/<id>")
def getMovieByCompany(id):
    page = request.args.get('page')

    moviesArray = {
        "results": [],
        "page" : page,
        "count": 0
    }

    movies = []

    if page and page.isdigit() :
        match = {"$match": { "production_companies.id": int(id) }}
        limit = {"$limit": 20}
        skip = {"$skip": 20 * (int(page) - 1)}
        movies = db.movies.aggregate([match, joinGenres, joinCompanies, addFields, project, skip, limit])
    
    for m in movies : 
        moviesArray["results"].append(m)
    
    moviesArray["count"] = len(moviesArray["results"])

    return jsonify(moviesArray)

@movie.route("/genre/<id>")
def getMovieByGenre(id):
    page = request.args.get('page')

    match = {"$match": {"genres.id": int(id)}}
    limit = {"$limit": 20}
    skip = {"$skip": 20 * (int(page) - 1)}
    movies = db.movies.aggregate([match, joinGenres, joinCompanies, addFields, project, skip, limit])
    
    data = {
        "results": [],
        "page" : page,
        "count": 0
    }
    
    for movie in movies: 
        data["results"].append(movie)
        
    data["count"] = len(data["results"])

    return jsonify(data)

@movie.route("/language/<originalLanguage>")
def getMovieByLanguage(originalLanguage):
    page = request.args.get('page')

    match = {"$match": {"original_language": {"$regex":originalLanguage}}}
    limit = {"$limit": 20}
    skip = {"$skip": 20 * (int(page) - 1)}
    movies = db.movies.aggregate([match, joinGenres, joinCompanies, addFields, project, skip, limit])
    
    data = {
        "results": [],
        "page" : page,
        "query": {
            "original_language": originalLanguage,
        },
        "count": 0
    }
    
    for movie in movies: 
        data["results"].append(movie)
        
    data["count"] = len(data["results"])

    return jsonify(data)

# http://127.0.0.1:5000/api/movie/runtime?page=1&max=130&min=125
@movie.route("/runtime")
def getMovieClassedByRuntime():
    page = request.args.get('page')
    minimum = request.args.get('min')
    maximum = request.args.get('max')

    limit = {"$limit": 20}
    skip = {"$skip": 20 * (int(page) - 1)}
    sort = {"$sort": {"runtime": -1}} 

    data = {
        "results": [],
        "page" : page,
        "query": {
            "min": minimum,
            "max": maximum
        },
        "count": 0
    }

    if maximum != None and minimum != None:
        match = { "$match": {"runtime": {"$gt": int(minimum) , "$lt": int(maximum) }}}
        print("a")
        movies = db.movies.aggregate([match, joinGenres, joinCompanies, addFields, project, skip, limit, sort])
    elif maximum != None:
        match = { "$match": {"runtime": {"$lt":  int(maximum)}}}
        print("b")
        movies = db.movies.aggregate([match, joinGenres, joinCompanies, addFields, project, skip, limit, sort])
    elif minimum != None:
        match = { "$match": {"runtime": {"$gt":  int(minimum)}}}
        print("c")
        movies = db.movies.aggregate([match, joinGenres, joinCompanies, addFields, project, skip, limit, sort])
    else:
        movies = db.movies.aggregate([joinGenres, joinCompanies, addFields, project, skip, limit, sort])
    
    for movie in movies: 
        data["results"].append(movie)

    data["count"] = len(data["results"])

    return jsonify(data)

# http://127.0.0.1:5000/api/movie/revenue/company?page=1
# @movie.route("/revenue/company")
# def getMovieByCompanyRevenue():
#     page = request.args.get('page')

#     project = { 
#     "$project": {
#         "_id": 1,
#         "genres._id" : 0,
#         "production_companies._id": 0
#     }
# }

#     moyenne = {"$group" : {"_id": "$production_companies.id" , "revenue" : { "$avg" : "$revenue" }} }
#     limit = {"$limit": 20}
#     skip = {"$skip": 20 * (int(page) - 1)}
#     sort = {"$sort": {"revenue": -1}} 
#     movies = db.movies.aggregate([moyenne, joinCompanies, addFields, project, skip, limit, sort])
    
#     data = {
#         "results": [],
#         "page" : page,
#         "count": 0
#     }
    
#     for movie in movies: 
#         data["results"].append(movie)
        
#     data["count"] = len(data["results"])

#     return jsonify(data)

# http://127.0.0.1:5000/api/movie/date?page=1&year=1995
@movie.route("/date")
def getMovieByDate():
    page = request.args.get('page')
    year = request.args.get('year')

    match = { "$match": {"release_date": {"$regex": year}}}
    limit = {"$limit": 20}
    skip = {"$skip": 20 * (int(page) - 1)}
    movies = db.movies.aggregate([match, joinGenres, joinCompanies, addFields, project, skip, limit])
    
    data = {
        "results": [],
        "query": {
            "year": year
        },
        "page" : page,
        "count": 0
    }
    
    for movie in movies: 
        data["results"].append(movie)
        
    data["count"] = len(data["results"])

    return jsonify(data)