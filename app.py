from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# enable cross-site origin requests
CORS(app)

@app.route('/')
def index():
    return jsonify([
        {
            '_id': 1,
            'name': 'Fluffy',
            'type': 'dog'
        }
    ])

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='localhost',
            port=8080,
            debug=True)