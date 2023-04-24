from App.models import Exercise
from App.database import db

def create_exercise(name, description, category):
    newExercise = Exercise(name=name, description=description, category=category)
    db.session.add(newExercise)
    db.session.commit()
    return newExercise

def get_exercise_by_name(name):
    return Exercise.query.filter_by(name=name).first()

def get_exercise_by_id(id):
    return Exercise.query.get(id)

def get_all_exercises():
    return Exercise.query.all()

def get_all_exercises_json():
    exercises = Exercise.query.all()
    if not exercises:
        return[]
    exercises = [exercise.get_json() for exercise in exercises]
    return exercises


