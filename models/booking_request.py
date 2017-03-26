from models.base import db
from models.user import User
from models.booking import Booking


class BookingRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.Date)
    booking_time = db.Column(db.Time)
    details = db.Column(db.String(240))
    booking_id = db.Column(db.Integer(), db.ForeignKey(Booking.id))
    worker_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    booking = db.relationship(Booking, foreign_keys=[booking_id])
    worker = db.relationship(User, foreign_keys=[worker_id])

    def __str__(self):
        return self.details


def add_booking_request(
        booking_id,
        booking_date,
        booking_time,
        details,
        worker_id):
    item = BookingRequest()
    item.booking_id = booking_id
    item.booking_date = booking_date
    item.booking_time = booking_time
    item.details = details
    item.worker_id = worker_id

    db.session.add(item)
    db.session.commit()

    return item.id


def approve_request(id):
    booking_request = BookingRequest.query.filter_by(id=id).one()
    booking = Booking.query.filter_by(id=booking_request.booking_id).one()

    booking.booking_date = booking_request.booking_date
    booking.booking_time = booking_request.booking_time
    booking.details = booking_request.details
    booking.worker_id = booking_request.worker_id
    booking.is_taken = True

    db.session.commit()
