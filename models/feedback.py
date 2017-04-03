from models.base import db
from models.user import User


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.Integer)
    feedback_date = db.Column(db.Date)
    details = db.Column(db.String(240))
    customer_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    customer = db.relationship(User, foreign_keys=[customer_id])
    worker_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    worker = db.relationship(User, foreign_keys=[worker_id])

    def __str__(self):
        return self.star


def add_feedback(
        star,
        feedback_date,
        details,
        customer_id,
        worker_id):
    item = Feedback()
    item.star = star
    item.feedback_date = feedback_date
    item.details = details
    item.customer_id = customer_id
    item.worker_id = worker_id

    db.session.add(item)
    db.session.commit()

    return item.id
