from flask_cors import CORS
from pymongo import MongoClient
import pymongo
import json
from flask import Flask, jsonify, request
app = Flask(__name__)


#MONGODB_URI = 'mongodb+srv://testuser:test123@cluster0.mlfc9.mongodb.net/test'
CORS(app)  # Added this for no access control origin cors policy error in frontend

client = pymongo.MongoClient(
    "mongodb+srv://testuser:test123@cluster0.mlfc9.mongodb.net/test?retryWrites=true&w=majority")
database = client.duckdata


@app.route("/", methods=["GET"])
def index():
    return "Hello index"


@app.route("/getducks", methods=["GET"])
def getducks():
    duck_list = []
    duck_collection = database.feed
    ducks = duck_collection.find({}, {'_id': 0})
    for document in ducks:
        duck_list.append(document)
    print(duck_list)
    return jsonify(duck_list)


@app.route("/addducks", methods=["GET", "POST"])
def addducks():

    duckdata = request.get_json()  # get the data from post request sent by client
    username = duckdata["username"]
    # Exract the fields required for db insertion
    feedtime = duckdata["feedtime"]
    food = duckdata["food"]
    location = duckdata["location"]
    number = duckdata["number"]
    quantity = duckdata["quantity"]

    print("Username = ", username)
    if not duckdata:
        err = {'ERROR': 'No data passed'}
        return jsonify(err)

    else:
        lastid = database.feed.find().sort([("id", -1)]).limit(1)
        # Maintaining own increment counter in database hence adding this
        id = int(lastid[0]["id"]) + 1

        print(id)

        if database.feed.find_one({'username': username}):
            if database.feed.find_one({'feedtime': feedtime}):
                return jsonify("Same user cannot feed at the same time");
        else:
            database.feed.insert({
                'id': str(id),
                'username': username,
                'feedtime': feedtime,
                'food': food,
                'location': location,
                'number': number,
                'quantity': quantity
            })
            return jsonify("Duck data added Successfully!")


if __name__ == '__main__':
    app.run()
