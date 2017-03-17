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
    role = db.Column(db.String(20))
    services = db.relationship(Service, secondary=user_services_table)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
