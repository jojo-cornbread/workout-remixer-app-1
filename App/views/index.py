from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
from App.controllers import create_user

from App.models import *
from App.controllers import (add_exerciseSet, delete_exerciseSet, get_all_exerciseSets_json)

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
        # exerciseSets_list = get_all_exerciseSets_json()

        # exerciseSets = set()

        # for exerciseSet in exerciseSets_list:
        #     exerciseSets.add(exerciseSet['name'])

        # for(exerciseSet in exerciseSets_list):
        #     if(exerciseSet.name)

        # return jsonify(categories)

    return render_template('index.html', categories = categories, exercises_list = exercises_list, exerciseSets = exerciseSets)

    # return something if the response bad?
    # else:
    #     return

@index_views.route('/add-exerciseSet/<int:id>', methods=['POST'])
@login_required
def add_ExerciseSet_action(id):
    data = request.form

    user = current_user

    # do a check for if the exercise set exist already
    # exerciseSet = get_exerciseSet_by_name(name)
    # if exerciseSet is not None:
    #     test = 1

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

@index_views.route('/delete-exerciseSet/<int:exerciseSet_id>', methods=['GET'])
@login_required
def delete_exerciseSet_action(exerciseSet_id):
    
    user = current_user

    res = delete_exerciseSet(exerciseSet_id)

    if res == None:
        flash('Invalid or unauthorized')
    else:
        flash('exercise set deleted!')
    return redirect(url_for('index_views.index_page'))

@index_views.route('/exerciseSet-info/<exerciseSet_name>', methods=['GET'])
@login_required
def get_exerciseSet_data_action(exerciseSet_name):

    user = current_user

    exerciseSets = get_all_exerciseSets_json()

    exerciseList = []
    # exerciseSets = [exerciseSet.get_json() for exerciseSet in exerciseSets]

    for exerciseSet in exerciseSets:
        if exerciseSet['name'] == exerciseSet_name:
            exerciseList.append(exerciseSet)

    if user:
        return render_template('user_info.html', exerciseList = exerciseList)
        
    else:
        flash('Invalid or unauthorize')
        return rediect(url_for('index_views.index_oage'))

# @app.route('/release-pokemon/<poke_user_id>', methods = ['GET'])
# @login_required 
# def release_pokemon_action(poke_user_id):
#   # pokemonName = UserPokemon.query.filter_by()
#   res = current_user.release_pokemon(poke_user_id)

#   if res == None:
#     flash('Invalid or unauthorized')
#   else:
#     flash('Pokemon Released!')
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

# hi
# helloo

# helllo again
# helllooooooooooooooooooooooooooooooooooooooo
#yayyyyyyyyyyyyyyyyyyyyyyyyyyyy