import requests, pymongo
from pprint import pprint

Mongo = pymongo.MongoClient("mongodb+srv://dbAdmin:azerty@cluster0.egcbs.mongodb.net/?retryWrites=true&w=majority")

# Mongo.drop_database('Cinema')

db = Mongo.Cinema
genres = db.genres
movies = db.movies
companies = db.companies


data = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=202f6ccc6b8b1135aea73bc1d66f1c91&language=en-US")

genres.insert_many(data.json()['genres'])

for i in range(0, 1000000):
    data = requests.get("https://api.themoviedb.org/3/company/" + str(i) +"?api_key=202f6ccc6b8b1135aea73bc1d66f1c91")

    if "success" not in data.json():
        companies.insert_one(data.json())
        # pprint(data.json())

