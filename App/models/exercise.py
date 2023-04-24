from App.database import db

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # may not need exercise_id
    # exercise_id = db.Column(db.Integer, nullable=False)

    description = db.Column(db.String, nullable=True)
    category = db.Column(db.Integer, nullable=False)

    

    # get_json function
    def get_json(self):
        return{
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "category":self.category
        }