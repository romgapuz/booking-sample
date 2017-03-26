from models.base import db
from models.user import User


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_type = db.Column(db.String(30))
    unit = db.Column(db.String(50))
    street = db.Column(db.String(50))
    city = db.Column(db.String(50))
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    user = db.relationship(User, backref='addresses')

    def __str__(self):
        return self.address_type


def add_address(
        id,
        address_type,
        unit,
        street,
        city):
    item = Address()
    item.address_type = address_type
    item.unit = unit
    item.street = street
    item.city = city
    item.user_id = id

    db.session.add(item)
    db.session.commit()

    return item.id
