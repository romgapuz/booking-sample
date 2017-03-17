from flask import jsonify
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound
from models.booking import Booking
from schema.booking import BookingSchema


def register(app):
    app.add_url_rule(
        '/booking/<id>',
        view_func=BookingIdApi.as_view('booking_id')
    )
    app.add_url_rule(
        '/customer/<id>/booking',
        view_func=CustomerIdBookingApi.as_view('customer_id_booking')
    )
    app.add_url_rule(
        '/worker/<id>/booking',
        view_func=WorkerIdBookingApi.as_view('worker_id_booking')
    )


class BookingIdApi(MethodView):
    def get(self, id):
        try:
            result = Booking.query.filter_by(id=id).one()
            return jsonify(BookingSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(BookingSchema(many=True).dump(None).data), 404


class CustomerIdBookingApi(MethodView):
    def get(self, id):
        try:
            result = Booking.query.filter_by(customer_id=id).all()
            return jsonify(BookingSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(BookingSchema(many=True).dump([]).data), 404


class WorkerIdBookingApi(MethodView):
    def get(self, id):
        try:
            result = Booking.query.filter_by(worker_id=id).all()
            return jsonify(BookingSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(BookingSchema(many=True).dump([]).data), 404
