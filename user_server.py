from flask import Flask, jsonify, request
import time
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://sanatthesanatsanat:sanatboiii@cluster0.fu9ig.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["jumper"]
collection = db["users_db"]


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"



# POSTS A USER TO THE DATABASE
@app.route('/users', methods=['POST'])
def post_user():
    request_data = request.get_json()
    new_user = {"_id": request_data['id'],
        'username': request_data['username'],
        'password': request_data['password']
    }

    # To deal with Pymongo disconnection error
    for i in range(5):
        try:
            collection.insert_one(new_user)
            break
        except pymongo.errors.AutoReconnect:
            time.sleep(pow(2, i))

    return jsonify(new_user)

# RETRIEVES USERS FROM DATABASE
@app.route('/users', methods=['GET'])
def get_users():
    users = collection.find()
    users_list = []
    for user in users:
        users_list.append(user)
    return jsonify({"users": users_list})

# RETRIEVES USER FROM DATABASE
@app.route('/users/<string:username>', methods=['GET'])
def get_user(username):
    users = collection.find()
    for user in users:
        if user['username'] == username:
            return jsonify(user)



if __name__ == '__main__':
    app.run(port=500)
