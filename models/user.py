from models.base import db
from models.service import Service

user_services_table = db.Table(
    'user_services',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    phone_no = db.Column(db.String(30))
    role = db.Column(db.String(20))
    services = db.relationship(Service, secondary=user_services_table)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


def add_customer(first_name, last_name, username, password, email, phone_no):
    user = User()
    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.password = password
    user.email = email
    user.phone_no = phone_no
    user.role = 'Customer'

    db.session.add(user)
    db.session.commit()

    return user.id


def update_customer(id, first_name, last_name, username, password, email, phone_no):
    user = User.query.filter_by(id=id).one()

    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if username is not None:
        user.username = username
    if password is not None:
        user.password = password
    if email is not None:
        user.email = email
    if phone_no is not None:
        user.phone_no = phone_no

    db.session.commit()
