import requests, pymongo
from pprint import pprint

Mongo = pymongo.MongoClient("mongodb+srv://dbAdmin:azerty@cluster0.egcbs.mongodb.net/?retryWrites=true&w=majority")


db = Mongo.Cinema
movies = db.movies

for i in range(0, 100000):
    data = requests.get("https://api.themoviedb.org/3/movie/" + str(i) + "?api_key=202f6ccc6b8b1135aea73bc1d66f1c91&language=en-US")
    movie = {}
    if "success" not in data.json():
        movie['id'] = data.json()["id"]
        movie['budget'] = data.json()["budget"]
        movie['genres'] = []

        for key in data.json()["genres"]:
            movie['genres'].append({"id": key["id"]})

        movie['homepage'] = data.json()["homepage"]
        movie['original_language'] = data.json()["original_language"]
        movie['original_title'] = data.json()["original_title"]
        movie['overview'] = data.json()["overview"]
        movie['popularity'] = data.json()["popularity"]
        movie['production_companies'] = []

        for key in data.json()["production_companies"]:
            movie['production_companies'].append({"id": key["id"]})

        movie['release_date'] = data.json()["release_date"]
        movie['revenue'] = data.json()["revenue"]
        movie['vote_count'] = data.json()["vote_count"]
        movie['vote_average'] = data.json()["vote_average"]
        movie['title'] = data.json()["title"]
        movie['tagline'] = data.json()["tagline"]
        movie['status'] = data.json()["status"]
        movie['runtime'] = data.json()["runtime"]

        movies.insert_one(movie)
        print(data.json()["id"])
        # pprint(movie)
