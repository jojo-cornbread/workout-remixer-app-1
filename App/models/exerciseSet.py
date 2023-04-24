from App.database import db
from .exercise import Exercise

class ExerciseSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exercises = db.relationship('Exercise', backref='exercise_set', lazy="dynamic")
    exercise = db.relationship('Exercise')

    def __init__(self, user_id, exercise_id, name):
        self.user_id = user_id
        self.exercise_id = exercise_id
        self.name = name

    def __repr__(self):
        return f'<ExerciseSet {self.id} : {self.name} user {self.user.username}>'

    def get_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'exercise': self.exercise.name,
            'user_id': self.user_id,
            'exercise_id':self.exercise_id
        }


