from pymongo import MongoClient

Mongo = MongoClient("mongodb+srv://dbAdmin:azerty@cluster0.egcbs.mongodb.net/?retryWrites=true&w=majority")

db = Mongo.Cinema