from flask import jsonify
from flask.views import MethodView
from flask import request
from sqlalchemy.orm.exc import NoResultFound
from models.booking import (
    Booking,
    add_booking,
    update_as_done
)
from schema.booking import BookingSchema
from models.booking_request import (
    BookingRequest,
    add_booking_request,
    approve_request
)
from schema.booking_request import BookingRequestSchema
import datetime


def register(app):
    """register the booking api endpoints"""
    app.add_url_rule(
        '/booking',
        view_func=BookingApi.as_view('booking')
    )
    app.add_url_rule(
        '/booking/<id>/done',
        view_func=BookingIdDoneApi.as_view('booking_id_done')
    )
    app.add_url_rule(
        '/booking/available',
        view_func=BookingAvailableApi.as_view('booking_available')
    )
    app.add_url_rule(
        '/booking/<id>',
        view_func=BookingIdApi.as_view('booking_id')
    )
    app.add_url_rule(
        '/booking/<id>/request',
        view_func=BookingIdRequestApi.as_view('booking_id_request')
    )
    app.add_url_rule(
        '/booking/request/<id>/approve',
        view_func=BookingRequestIdApproveApi.as_view(
            'booking_request_id_approve'
        )
    )
    app.add_url_rule(
        '/customer/<id>/booking',
        view_func=CustomerIdBookingApi.as_view('customer_id_booking')
    )
    app.add_url_rule(
        '/worker/<id>/booking',
        view_func=WorkerIdBookingApi.as_view('worker_id_booking')
    )


class BookingApi(MethodView):
    def post(self):
        """create booking"""
        try:
            booking_date = datetime.datetime.strptime(request.form['booking_date'], "%m/%d/%Y").date()
            booking_time = datetime.datetime.strptime(request.form['booking_time'], '%I:%M %p').time()
            details = request.form['details']
            service_name = request.form['service_name']
            customer_id = request.form['customer_id']
            worker_id = request.form['worker_id'] \
                if 'worker_id' in request.form else None

            add_booking(
                booking_date,
                booking_time,
                details,
                service_name,
                customer_id,
                worker_id
            )
        except Exception, ex:
            return "Error creating booking: {}". \
                format(repr(ex)), 400

        return jsonify(BookingSchema(many=False).dump(None).data), 201


class BookingIdDoneApi(MethodView):
    def put(self, id):
        """Update booking as done"""
        try:
            update_as_done(id)
        except Exception, ex:
            return "Error updating booking as done: {}". \
                format(repr(ex)), 400

        return jsonify(BookingSchema(many=False).dump(None).data), 200


class BookingAvailableApi(MethodView):
    def get(self):
        """get available booking by service ids"""
        try:
            result = Booking.query.filter_by(
                is_taken=False,
                worker_id=None
            ).all()
            return jsonify(BookingSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(BookingSchema(many=True).dump([]).data), 404


class BookingIdApi(MethodView):
    def get(self, id):
        """get booking by id"""
        try:
            result = Booking.query.filter_by(id=id).one()
            return jsonify(BookingSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(BookingSchema(many=True).dump(None).data), 404


class BookingIdRequestApi(MethodView):
    def get(self, id):
        """(customer) view requests for booking"""
        try:
            result = BookingRequest.query.filter_by(booking_id=id).one()
            return jsonify(BookingRequestSchema(many=False).dump(result).data)
        except NoResultFound:
            return jsonify(BookingRequestSchema(many=False).dump(None).data), 404

    def post(self, id):
        """(worker) create request for booking"""
        try:
            booking_date = datetime.datetime.strptime(request.form['booking_date'], "%m/%d/%Y").date()
            booking_time = datetime.datetime.strptime(request.form['booking_time'], '%I:%M %p').time()
            details = request.form['details']
            worker_id = request.form['worker_id']

            add_booking_request(
                id,
                booking_date,
                booking_time,
                details,
                worker_id
            )
        except Exception, ex:
            return "Error creating booking request: {}". \
                format(repr(ex)), 400

        return jsonify(BookingRequestSchema(many=False).dump(None).data), 201


class BookingRequestIdApproveApi(MethodView):
    def put(self, id):
        """(customer) approve booking request"""
        try:
            approve_request(id)
        except Exception, ex:
            return "Error approving booking request: {}". \
                format(repr(ex)), 400

        return jsonify(BookingRequestSchema(many=False).dump(None).data), 200


class CustomerIdBookingApi(MethodView):
    def get(self, id):
        """get bookings by customer id"""
        try:
            result = Booking.query.filter_by(customer_id=id).all()
            return jsonify(BookingSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(BookingSchema(many=True).dump([]).data), 404


class WorkerIdBookingApi(MethodView):
    def get(self, id):
        """get bookings by worker id"""
        try:
            result = Booking.query.filter_by(worker_id=id).all()
            return jsonify(BookingSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(BookingSchema(many=True).dump([]).data), 404
