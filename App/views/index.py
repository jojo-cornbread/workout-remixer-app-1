from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
from App.controllers import create_user

from App.models import *
from App.controllers import (add_exerciseSet)

from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

import requests
import json

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/app', methods=['GET'])
@index_views.route('/app/<int:category>', methods=['GET'])
#need to set up login things
@login_required
def index_page(category = 1):

    url = 'https://wger.de/api/v2/exercisecategory/?format=json'

    response = requests.get(url)

    if response.status_code == 200:
        
        categories = response.json()
        categories = categories['results']

        exercises_list = Exercise.query.filter_by(category=category)

        exerciseSets = ExerciseSet.query.filter_by(user_id = current_user.id)

        # return jsonify(categories)

    return render_template('index.html', categories = categories, exercises_list = exercises_list, exerciseSets = exerciseSets)

    # return something if the response bad?
    # else:
    #     return

@index_views.route('/exercise/<int:id>', methods=['POST'])
@login_required
def add_ExerciseSet_action(id):
    data = request.form

    user = current_user

    # do a check for if the exercise set exist already
    # exerciseSet = get_exerciseSet_by_name(name)


    # if exerciseSet is not None:
    #     test = 1

    # add_exerciseSet(exerciseSetName, userID, id)
    add_exerciseSet(data['exerciseSet_name'], user.id, id)

    if user:
        flash("Exercise added to Set!")
    else:
        flash("Unauthorized")
    return redirect(url_for('index_views.index_page'))

# capture route from assignment2
# @app.route('/pokemon/<pokemon_id>', methods = ['POST'])
# @login_required
# def capture_pokemon_action(pokemon_id):
#   data = request.form
#   # pokemon = Pokemon.query.all()
#   # userPokemon = UserPokemon.query.filter_by(pokemon_id = id)
#   user = current_user
#   user.catch_pokemon(pokemon_id, data['pokemon_name'])
    
#   if user:
#     flash("Pokemon captured!")
#   else:
#     flash("Unauthorized")
#   return redirect(url_for('home_page'))

# @index_views.route('/init', methods=['GET'])
# def init():
#     db.drop_all()
#     db.create_all()
#     create_user('bob', 'bobpass')
#     return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

    