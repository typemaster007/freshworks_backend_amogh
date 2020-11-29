import pymongo
import json
from flask import Flask, jsonify, request
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

@app.route("/addducks", methods=["GET","POST"])
def addducks():
 	
	duckdata = request.get_json()       #get the data from post request sent by client
	username = duckdata["username"]
	feedtime = duckdata["feedtime"]		#Exract the fields required for db insertion
	food = duckdata["food"]
	location = duckdata["location"]
	number = duckdata["number"]
	quantity = duckdata["quantity"]

	print("Username = ", username)
	if not duckdata:					
	    err = {'ERROR': 'No data passed'}
	    return jsonify(err)
	
	else:

	    lastid = database.feed.find().sort([("id",-1)]).limit(1)	#Maintaining own increment counter in database hence adding this
	    id = int(lastid [0]["id"]) + 1
	    
	    print(id)

	    #Adding the extracted field to MongoDB Duck feed table
	    database.feed.insert({
	    	'id': str(id),
	    	'username': username,
	    	'feedtime': feedtime,
	    	'food': food, 
	    	'location': location,
	    	'number' : number,
	    	'quantity' : quantity
	    	})

	return jsonify("Duck data added Successfully!")

if __name__ == '__main__':
    app.run()