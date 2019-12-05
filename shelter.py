from flask import Flask, render_template, request, redirect, url_for
import os

import pymongo

from bson.objectid import ObjectId

MONGO_URI = "mongodb+srv://root:asd1234@cluster0-rra3w.mongodb.net/test?retryWrites=true&w=majority"
DATABASE_NAME = "animal_shelter"


def get_connection():
    conn = pymongo.MongoClient(MONGO_URI)
    return conn


app = Flask(__name__)


@app.route('/')
def index():
    conn = get_connection()
    animals = conn[DATABASE_NAME]['animals'].find()
    return render_template('index.template.html', results=animals)


@app.route('/add-animal')
def show_add_animal_form():
    return render_template('add_animal.template.html')


@app.route('/add-animal', methods=['POST'])
def process_add_animal_form():
    animal_name = request.form.get('animal-name')
    breed = request.form['breed']
    microchip = request.form['microchip']

    conn = get_connection()
    conn[DATABASE_NAME]['animals'].insert({
        "name": animal_name,
        "breed": breed,
        "microchip": microchip
    })

    # redirect back to root url
    return redirect("/")


# /edit-animal/f2fa2da
@app.route('/edit-animal/<animal_id>')
def show_edit_animal_form(animal_id):
    conn = get_connection()
    animal = conn[DATABASE_NAME]['animals'].find_one({
        '_id': ObjectId(animal_id)
    })

    return render_template('edit_animal.template.html', animal=animal)


@app.route("/edit-animal/<animal_id>", methods=['POST'])
def process_edit_animal_form(animal_id):
    animal_name = request.form.get('animal-name')
    breed = request.form['breed']
    microchip = request.form['microchip']

    conn = get_connection()
    conn[DATABASE_NAME]["animals"].update({
        '_id': ObjectId(animal_id)
    }, {
        'name': animal_name,
        'breed': breed,
        'microchip': microchip
    })

    return redirect("/")


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='localhost',
            port=8081,
            debug=True)