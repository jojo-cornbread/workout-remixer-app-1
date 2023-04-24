from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required, login_user, logout_user

from.index import index_views

from App.models import *

import requests
import json

from App.controllers import (
    create_user,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_all_exerciseSets,
    get_all_exercises,
    get_exercise_by_id,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/', methods=['GET'])
@user_views.route('/login', methods=['GET'])
def login_page():
  if current_user.is_authenticated:
    return redirect('/app')
  return render_template('login.html', user=user)

@user_views.route('/login', methods=['POST'])
def login_action():

  data = request.form
  user = User.query.filter_by(username=data['username']).first()
  if user and user.check_password(data['password']):  # check credentials
    flash('Logged in successfully.')  # send message to next page
    login_user(user)  # login the user
    return redirect('/app')  # redirect to main page if login successful
  else:
    flash('Invalid username or password')  # send message to next page
  return redirect('/')

@user_views.route('/logout', methods=['GET'])
def logout_action():
  logout_user()
  return redirect('/')

@user_views.route('/signup', methods=['GET'])
def signup_page():
  return render_template('users.html')


@user_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form
    newUser = create_user(data['username'], data['email'], data['password'])

    try:
        db.session.add(newUser)
        db.session.commit()
        login_user(newUser)
        flash('Account Created!')
        return redirect(url_for('index_views.index_page'))
    except Exception:
        db.session.rollback()
        flash("Username or email already exists")
    return redirect(url_for('signup_page'))

# @app.route('/signup', methods = ['POST'])
# def signup_action():
#   data = request.form
#   newUser = User(username = data['username'], email = data['email'], password = data['password'])

#   try:
#     db.session.add(newUser)
#     db.session.commit()
#     login_user(newUser)
#     flash('Account Created!')
#     return redirect(url_for('home_page'))
#   except Exception:
#     db.session.rollback()
#     flash("username or email already exists")
#   return redirect(url_for('signup_page'))



@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'], data['email'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['email'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

  
@user_views.route('/user_info', methods=['GET', 'POST'])
def userInfo_page():
  exercises = []
  user = current_user
  xss = get_all_exerciseSets()
  for xs in xss:
    if xs.user_id == user.id:
      exercises.append(get_exercise_by_id( xs.exercise_id))
  cises = get_all_exercises()
  return render_template('user_info.html', user=user, xss=xss, cises=cises, exercises=exercises)

@user_views.route('/profile', methods=['GET'])
def get_profile():
    return render_template('profile.html')