from App.models import ExerciseSet
from App.database import db

from App.controllers import (
    get_exercise_by_id,
)

def create_exerciseSet(name, user_id, exercise_id):
    newExerciseSet = ExerciseSet(user_id=user_id, exercise_id=exercise_id, name=name)
    db.session.add(newExerciseSet)
    db.session.commit()
    return newExerciseSet


def add_exercise_to_set(set_id, exercise_id):
    eSet = get_exerciseSet_by_id(set_id)
    cise = get_exercise_by_id(exercise_id)
    if eSet:
        if cise:
            eSet.exercises.append(cise)
            db.session.add(eSet)
            db.session.commit()
            return eSet
    return False
    

def get_exerciseSet_by_name(name):
    return ExerciseSet.query.filter_by(name=name).first()

def get_exerciseSet_by_id(id):
    return ExerciseSet.query.get(id)

def get_all_exerciseSets():
    return ExerciseSet.query.all()

def get_all_exerciseSets_json():
    exerciseSets = ExerciseSet.query.all()

    if not exerciseSets:
        return []
    
    exerciseSets = [exerciseSet.get_json() for exerciseSet in exerciseSets]
    return exerciseSets


