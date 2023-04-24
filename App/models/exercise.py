from App.database import db

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    exercise_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)
    category = db.Column(db.Integer, nullable=False)

    

    # get_json function
    def get_json(self):
        return{
            "id":self.id,
            "name":self.name,
            "exercise_id":self.exercise_id,
            "description":self.description,
            "category":self.category
        }