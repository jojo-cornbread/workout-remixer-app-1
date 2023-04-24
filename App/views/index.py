from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
from App.controllers import create_user

from App.models import *
from App.controllers import (
    add_exerciseSet, 
    delete_exerciseSet, 
    get_all_exerciseSets, 
    get_all_exerciseSets_json, 
    get_exercise_by_id, 
    add_exercise_to_set,
    get_exerciseSet_by_name,
    get_exercise_by_name,
)

from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

import requests
import json

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/app', methods=['GET'])
@index_views.route('/app/<int:category>', methods=['GET'])
#need to set up login things
@login_required
def index_page(category = 10):
    user = current_user
    url = 'https://wger.de/api/v2/exercisecategory/?format=json'

    response = requests.get(url)

    if response.status_code == 200:
        
        categories = response.json()
        categories = categories['results']

        exercises_list = Exercise.query.filter_by(category=category)

        exerciseSets = ExerciseSet.query.filter_by(user_id = current_user.id)
       
    return render_template('index.html', categories = categories, exercises_list = exercises_list, exerciseSets = exerciseSets, user=user)


@index_views.route('/add-exerciseSet/<int:id>', methods=['POST'])
@login_required
def add_ExerciseSet_action(id):
    data = request.form

    user = current_user
    exercise = get_exercise_by_id(id)

    setName = data['exerciseSet_name']

    # do a check for if the exercise set exist already
    sets = []
    xss = get_all_exerciseSets()
    for xs in xss:
        if xs.user_id == user.id:
            sets.append(xs)

    for set in sets:
        if set.name == setName:
            flash("Exercise added to set!")
            add_exercise_to_set(set.id, id)
            return redirect('/app')
    
    add_exerciseSet(setName, user.id, id)

    if user:
        flash("Exercise added to Set!")
    else:
        flash("Unauthorized")
    return redirect(url_for('index_views.index_page'))


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

@index_views.route('/delete-exercise/<int:exercise_id>', methods=['GET'])
@login_required
def delete_exercise_action(exercise_id):
    
    user = current_user

    res = delete_exerciseSet(exercise_id)

    if res == None:
        flash('Invalid or unauthorized')
    else:
        flash('exercise deleted!')
    return redirect(url_for('user_views.userInfo_page'))

@index_views.route('/exerciseSet-info/<exerciseSet_name>', methods=['GET'])
@login_required
def get_exerciseSet_data_action(exerciseSet_name):
    user = current_user

    eSet = get_exerciseSet_by_name(exerciseSet_name)
    cises = []

    for exercise in eSet.exercises:
        cises.append(exercise)

    if user:
        return render_template('sets.html', set=eSet, cises=cises)
        
    else:
        flash('Invalid or unauthorize')
        return rediect(url_for('index_views.index_oage'))

@index_views.route('/exercise-info/<exercise>', methods=['GET'])
@login_required
def exercise_info(exercise):
    user = current_user

    cise = get_exercise_by_name(exercise)

    if user:
        return render_template('profile.html', cise=cise)
        
    else:
        flash('Invalid or unauthorize')
        return rediect(url_for('index_views.index_oage'))


@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
