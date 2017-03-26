from models.base import db
from models.user import User
from models.service import Service
from models.address import Address


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.Date)
    booking_time = db.Column(db.Time)
    details = db.Column(db.String(240))
    is_taken = db.Column(db.Boolean)
    is_done = db.Column(db.Boolean)
    service_name = db.Column(db.String(100), db.ForeignKey(Service.name))
    service = db.relationship(Service, backref='service')
    customer_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    customer = db.relationship(User, foreign_keys=[customer_id])
    customer_address_id = db.Column(db.Integer(), db.ForeignKey(Address.id))
    customer_address = db.relationship(Address, foreign_keys=[customer_address_id])
    worker_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    worker = db.relationship(User, foreign_keys=[worker_id])

    def __str__(self):
        return 'Need "{}" by "{} {}" on "{} {}"'.format(
            self.service.name,
            self.customer.first_name,
            self.customer.last_name,
            self.booking_date,
            self.booking_time
        )


def add_booking(
        booking_date,
        booking_time,
        details,
        service_name,
        customer_id,
        customer_address_id,
        worker_id):
    item = Booking()
    item.booking_date = booking_date
    item.booking_time = booking_time
    item.details = details
    item.service_name = service_name
    item.customer_id = customer_id
    item.customer_address_id = customer_address_id
    item.worker_id = worker_id
    item.is_taken = False
    item.is_done = False

    db.session.add(item)
    db.session.commit()

    return item.id


def update_as_done(id):
    item = Booking.query.filter_by(id=id).one()
    item.is_done = True

    db.session.commit()


def approve_customer_booking(id):
    item = Booking.query.filter_by(id=id).one()
    item.is_taken = True

    db.session.commit()
