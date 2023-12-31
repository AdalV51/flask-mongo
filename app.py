import random
from flask import Flask, jsonify
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient(
    "mongodb://mongo-db:27017",
    username="adal",
    password="password",
    authSource="admin",
    authMechanism="SCRAM-SHA-256",
)

db = client["miapp"]
collection = db["customers"]


# Create a function to get a random name
def get_name():
    names = [
        "John",
        "Mary",
        "Bob",
        "Jane",
        "Peter",
        "Paul",
        "Mark",
        "Luke",
        "Matthew",
        "James",
    ]
    return random.choice(names)


# Create a function to get a random address
def get_address():
    addresses = [
        "Highway 37",
        "Main Street",
        "First Avenue",
        "Second Street",
        "Park Avenue",
        "Elm Street",
        "Maple Avenue",
        "Oak Street",
        "Washington Avenue",
        "Lake Street",
    ]
    return random.choice(addresses)


# Create a function to get a dict with a random name and address
def get_record():
    record = {"name": get_name(), "address": get_address()}
    return record


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, Docker!"


@app.route("/add")
def add_record():
    record = get_record()
    collection.insert_one(record)
    record["_id"] = str(record["_id"])
    return jsonify(record)


@app.route("/list")
def list_records():
    records = []
    for record in collection.find():
        record["_id"] = str(record["_id"])
        records.append(record)
    return jsonify(records)


@app.route("/delete-all")
def delete_all():
    collection.delete_many({})
    return jsonify({"message": "All records deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
