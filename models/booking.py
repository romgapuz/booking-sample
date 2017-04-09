from models.base import db
from models.user import User
from models.service import Service


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.Date)
    booking_time = db.Column(db.Time)
    details = db.Column(db.String(240))
    address = db.Column(db.String(200))
    is_taken = db.Column(db.Boolean)
    is_done = db.Column(db.Boolean)
    is_cancel = db.Column(db.Boolean)
    service_name = db.Column(db.Integer, db.ForeignKey(Service.name))
    service = db.relationship(Service, backref='service')
    customer_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    customer = db.relationship(User, foreign_keys=[customer_id])
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
        address,
        customer_id,
        worker_id):
    item = Booking()
    item.booking_date = booking_date
    item.booking_time = booking_time
    item.details = details
    item.service_name = service_name
    item.address = address
    item.customer_id = customer_id
    item.worker_id = worker_id
    item.is_taken = False
    item.is_done = False

    db.session.add(item)
    db.session.commit()

    return item.id


def update_booking(
        id,
        booking_date,
        booking_time,
        details,
        address,
        is_taken,
        is_done,
        is_cancel):
    booking = Booking.query.filter_by(id=id).one()

    if booking_date is not None:
        booking.booking_date = booking_date
    if booking_time is not None:
        booking.booking_time = booking_time
    if details is not None:
        booking.details = details
    if address is not None:
        booking.address = address
    if is_taken is not None:
        booking.is_taken = is_taken
    if is_done is not None:
        booking.is_done = is_done
    if is_cancel is not None:
        booking.is_cancel = is_cancel

    db.session.commit()


def update_as_done(id):
    item = Booking.query.filter_by(id=id).one()
    item.is_done = True

    db.session.commit()


def approve_customer_booking(id):
    item = Booking.query.filter_by(id=id).one()
    item.is_taken = True

    db.session.commit()
