from models.base import db
from models.user import User


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.Integer)
    feedback_date = db.Column(db.Date)
    details = db.Column(db.String(240))
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    user = db.relationship(User, backref='feedbacks')

    def __str__(self):
        return self.star
