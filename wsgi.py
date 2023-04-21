import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app

# import the other controllers
from App.controllers import ( create_user, get_all_users_json, get_all_users)
from App.controllers import ( create_exercise, get_all_exercises_json, get_all_exercises)

import requests
import json
# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob','bob@mail.com', 'bobpass')

    # add all the exercises here
    url = 'https://wger.de/api/v2/exercise/?format=json&limit=200'

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
            if(data['results'][i]['language'] == 2):
                #print the name of the exericse
                # print(data['results'][i]['name'])
                create_exercise(data['results'][i]['name'], data['results'][i]['description'], data['results'][i]['category'])


        # NOW YOU CAN ADD IN THE EXERCISES TO THE DATABASE BY FILTERING THE INFORMATION NEEDED

    print('database intialized')

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

