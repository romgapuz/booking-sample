from models import (
    db,
    User
)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime)
    is_read = db.Column(db.Boolean)

    sender_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    sender = db.relationship(User, foreign_keys=[sender_id])
    receiver_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    receiver = db.relationship(User, foreign_keys=[receiver_id])