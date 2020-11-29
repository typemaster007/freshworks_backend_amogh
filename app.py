import pymongo
from flask import Flask
app = Flask(__name__)


MONGODB_URI = 'mongodb+srv://testuser:<password>@cluster0.mlfc9.mongodb.net/test'

@app.route("/", methods=["GET"])
def index():
    app.logger.info('Welcome to Index')
    return "Hello index"

if __name__ == '__main__':
    app.run()