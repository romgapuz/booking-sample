from models import (
    db,
    User,
    Service
)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.Date)
    booking_time = db.Column(db.Time)
    details = db.Column(db.String(240))
    is_taken = db.Column(db.Boolean)
    
    service_name = db.Column(db.String(100), db.ForeignKey(Service.name))
    service = db.relationship(Service, backref='service')
    customer_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    customer = db.relationship(User, foreign_keys=[customer_id])
    worker_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    worker = db.relationship(User, foreign_keys=[worker_id])

    def __str__(self):
        return self.service