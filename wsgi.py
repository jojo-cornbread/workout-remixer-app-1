import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app

# import the other controllers
# user controller
# from App.controllers import ( create_user, get_all_users_json, get_all_users)
from App.controllers import *
#exercise controller
# from App.controllers import ( create_exercise, get_all_exercises_json, get_all_exercises)
#exerciseSet controller
# from App.controllers import (create_exerciseSet, get_all_exerciseSets_json, get_all_exerciseSets)

import requests
import json
# This commands file allow you to create convenient CLI commands for testing controllers

#hi sabrina
#hi Josiah
#cryBuddies lmaooo
# depression

# hello again
#hello from the other side
app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob','bob@mail.com', 'bobpass')

    print('database intialized')

@app.cli.command("get-data", help="Creates and initializes the data from the api")
def get_data():
    # add all the exercises here
    url = 'https://wger.de/api/v2/exercise/?format=json&limit=800'

    # https://wger.de/api/v2/exercise/?format=json&limit=200 sets the amount of exercises
    # to a limit of 200, the limit can be altered or removed
    
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        
        data = response.json()
        # data = json.loads(data)
        
        # print(data)
        # print(response.content)

        # print the first entry in the results list in data
        # print(data['results'][0])

        # this loops through th size of the data['results'] and if the language == 2 (english)
        # then print the exercise name
        for i in range (len(data['results'])):
            
            if(data['results'][i]['id']) == 91:
                    print(data['results'][i]['description'])


            if(data['results'][i]['language'] == 2):
                #print the name of the exericse
                # print(data['results'][i]['name'])
                create_exercise(data['results'][i]['name'],data['results'][i]['id'], data['results'][i]['description'], data['results'][i]['category'])

            
        # NOW YOU CAN ADD IN THE EXERCISES TO THE DATABASE BY FILTERING THE INFORMATION NEEDED
    
    # add in methods to the user controller to add exercises to a set,
    # look at the captre pokemon etc in assignment2 models


    user = get_user_by_username('bob')
    user = user.get_json()
    # print(user['id'])

    exerciseSetName = "oogabooga"

    testExerciseID = get_exercise_by_id(1)
    testExerciseID = testExerciseID.get_json()
    # print(testExerciseID['id'])

    add_exerciseSet(exerciseSetName ,user['id'], testExerciseID['id'])

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("email", default="rob@mail.com")
@click.argument("password", default="robpass")
def create_user_command(username, email, password):
    create_user(username, email, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Exercise Commands
'''

exercise_cli = AppGroup('exercise', help='Exercise object commands')

@exercise_cli.command("list", help="Lists all exercises in the database")
@click.argument("format", default="string")
def list_exercise_command(format):
    if format == 'string':
        print(get_all_exercises())
    else:
        print(get_all_exercises_json())

app.cli.add_command(exercise_cli)

'''
ExerciseSet Commands
'''
exerciseSet_cli = AppGroup('exerciseSet', help='ExerciseSet object commands')

@exerciseSet_cli.command("list", help="Lists all exerciseSets in the database")
@click.argument("format", default="string")
def list_exerciseSet_command(format):
    if format == 'string':
        print(get_all_exerciseSets())
    else:
        print(get_all_exerciseSets_json())

@exerciseSet_cli.command("sort-name", help="returns a list of all exerciseSets by name")
# @click.argument("format", default="string")
@click.argument("name", default="")
def sort_name_exerciseSet_command(name):
    if name == '':
        # exerciseSets = ExerciseSet.query.filter_by(name=name).all()
        print("No name entered")
    else:
        exerciseSets = get_all_exerciseSets_json()

        for exerciseSet in exerciseSets:
            if(exerciseSet['name'] == name):
                print(exerciseSet)

app.cli.add_command(exerciseSet_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

