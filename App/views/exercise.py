from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (
    create_exercise,
    jwt_authenticate, 
    get_all_exercises,
    get_all_exercises_json,
    jwt_required
)

exercise_views = Blueprint('exercise_views', __name__, template_folder='../templates')

@exercise_views.route('/api/exercises', methods=['GET'])
def get_exercises_action():
    exercises = get_all_exercises_json()
    return jsonify(exercises)

# @user_views.route('/api/users', methods=['GET'])
# def get_users_action():
#     users = get_all_users_json()
#     return jsonify(users)