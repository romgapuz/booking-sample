from models.base import db
from models.user import User
import string
import random


class ResetPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80))
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    user = db.relationship(User, foreign_keys=[user_id])

    def __str__(self):
        return self.username


def create_password(id):
    item = ResetPassword()
    item.password = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        ) for _ in range(6)
    )
    item.user_id = id

    db.session.add(item)
    db.session.commit()

    return item.id


def apply_password(id):
    new_password = ResetPassword.query.filter_by(id=id).one()

    user = User.query.filter_by(id=new_password.user_id).one()
    user.password = new_password.password

    db.session.commit()

    return new_password.password
