from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from bson.json_util import dumps
from bson import json_util
import json
import pymongo
import os
from bson.objectid import ObjectId

MONGO_URI = "mongodb+srv://root:asd1234@cluster0-rra3w.mongodb.net/test?retryWrites=true&w=majority"
DATABASE_NAME = "animal_shelter"

app = Flask(__name__)
# enable the cross origin
CORS(app)

def get_connection():
    conn = pymongo.MongoClient(MONGO_URI)
    return conn

@app.route('/')
def index():
    conn = get_connection()
    # where we get data from Mongo (can replace with MySQL)
    animals = conn[DATABASE_NAME]['animals'].find()
    return dumps(animals) #important - return as JSON


@app.route('/newAnimal', methods=['POST'])
def addAnimal():
    animal_name = request.json.get('animal-name')
    breed = request.json['breed']
    microchip = request.json['microchip']

    conn = get_connection()
    new_animal_id = conn[DATABASE_NAME]['animals'].insert({
        "name": animal_name,
        "breed": breed,
        "microchip": microchip
    })

    new_animal = conn[DATABASE_NAME]['animals'].find_one({
        '_id':ObjectId(new_animal_id)
    })

    return dumps(new_animal)

@app.route('/updateAnimal/<animal_id>', methods=['PUT'])
def updateAnimal(animal_id):
    animal_name = request.json.get('animal-name')
    breed = request.json['breed']
    microchip = request.json['microchip']

    conn = get_connection()
    conn[DATABASE_NAME]['animals'].update({
        '_id': ObjectId(animal_id)
    }, {
        'name' : animal_name,
        'breed' : breed,
        'microchip' : microchip
    })
    new_animal = conn[DATABASE_NAME]['animals'].find_one({
        '_id': ObjectId(animal_id)
    })
    return dumps(new_animal)

@app.route('/deleteAnimal/<animal_id>', methods=['DELETE'])
def delete(animal_id):
    conn = get_connection()

    conn[DATABASE_NAME]['animals'].delete_one({
        '_id':ObjectId(animal_id)
    })

    return jsonify({
        'status': True
    })

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='localhost',
            port=8081,
            debug=True)