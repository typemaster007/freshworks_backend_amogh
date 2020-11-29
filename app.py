import pymongo
import json
from flask import Flask, jsonify
app = Flask(__name__)
from pymongo import MongoClient


#MONGODB_URI = 'mongodb+srv://testuser:test123@cluster0.mlfc9.mongodb.net/test'

client = pymongo.MongoClient("mongodb+srv://testuser:test123@cluster0.mlfc9.mongodb.net/test?retryWrites=true&w=majority")
database = client.duckdata



@app.route("/", methods=["GET"])
def index():
    return "Hello index"

@app.route("/getducks", methods=["GET"])
def getducks():
    duck_collection = database.feed
    ducks = duck_collection.find({}, {'_id': 0})
    duck_list = list(ducks)
    return jsonify(duck_list)

if __name__ == '__main__':
    app.run()