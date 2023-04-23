from App.models import ExerciseSet
from App.database import db

def create_exerciseSet(name, user_id, exercise_id):
    newExerciseSet = ExerciseSet(user_id=user_id, exercise_id=exercise_id, name=name)
    db.session.add(newExerciseSet)
    db.session.commit()
    # print('new exercise set created')
    return newExerciseSet

# different methods we may need later on
# get_exerciseSet_user()
# def addExercise(name, user_id, exercise_id):
#     exerciseSet = get_exerciseSet_by_name(name)

#     exerciseSet




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


# def create_exercise(name, description, category):
#     newExercise = Exercise(name=name, description=description, category=category)
#     db.session.add(newExercise)
#     db.session.commit()
#     return newExercise

# def get_exercise_by_name(name):
#     return Exercise.query.filter_by(name=name).first()

# def get_exercise_by_id(id):
#     return Exercise.query.get(id)

# def get_all_exercises():
#     return Exercise.query.all()

# def get_all_exercises_json():
#     exercises = Exercise.query.all()
#     if not exercises:
#         return[]
#     exercises = [exercise.get_json() for exercise in exercises]
#     return exercises