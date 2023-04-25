from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user

import requests
import json

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():

    url = 'https://wger.de/api/v2/exercisecategory/?format=json'

    response = requests.get(url)

    if response.status_code == 200:
        
        categories = response.json()
        categories = categories['results']

        # return jsonify(categories)

    return render_template('index.html', categories = categories)

    # return render_template("home.html", pokemon = pokemon, pokemon_sel = pokemon_sel)

# @index_views.route('/init', methods=['GET'])
# def init():
#     db.drop_all()
#     db.create_all()
#     create_user('bob', 'bobpass')
#     return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})