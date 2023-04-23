from App.database import db

class ExerciseSet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    name = db.Column(db.String, nullable = False, unique=True)

    # ???
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
            'user_id': self.user_id
        }


#     def __init__(self, user_id, pokemon_id, name):
#     self.user_id = user_id
#     self.pokemon_id = pokemon_id
#     self.name = name
  
#   def __repr__(self):
#       return f'<UserPokemon {self.id} : {self.name} trainer {self.user.username}>'

# def get_json(self):
#     return{
#       'id': self.id,
#       'name': self.name,
#       'species': self.pokemon.name
#     }