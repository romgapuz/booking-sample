from flask import jsonify
from flask.views import MethodView
from flask import request
from sqlalchemy.orm.exc import NoResultFound
from models.booking import (
    Booking,
    add_booking,
    update_as_done,
    approve_customer_booking,
    update_booking
)
from models.user import User
from models.service import Service
from schema.booking import BookingSchema
from models.booking_request import (
    BookingRequest,
    add_booking_request,
    approve_request,
    reject_request
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
        '/booking/taken',
        view_func=BookingTakenApi.as_view('booking_taken')
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
        '/booking/request/<id>/reject',
        view_func=BookingRequestIdRejectApi.as_view(
            'booking_request_id_reject'
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
    app.add_url_rule(
        '/worker/booking/<id>/approve',
        view_func=WorkerBookingIdApproveApi.as_view(
            'worker_booking_id_approve'
        )
    )


class BookingApi(MethodView):
    def post(self):
        """create booking"""
        try:
            booking_date = datetime.datetime.strptime(request.form['booking_date'], "%m/%d/%Y").date()
            booking_time = datetime.datetime.strptime(request.form['booking_time'], '%I:%M %p').time()
            details = request.form['details']
            service_name = request.form['service_name']
            address = request.form['address']
            customer_id = request.form['customer_id']
            worker_id = request.form['worker_id'] \
                if 'worker_id' in request.form else None

            add_booking(
                booking_date,
                booking_time,
                details,
                service_name,
                address,
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
        worker_id = request.args.get('worker_id', None)
        customer_id = request.args.get('customer_id', None)

        if worker_id and customer_id:
            return 'Either the worker_id and ' + \
                'customer_id should be provided', 400

        try:
            if worker_id:
                result = Booking.query.filter_by(
                    is_taken=False,
                    is_done=False,
                    is_cancel=False,
                    worker_id=None
                ).join(
                    Service,
                    Booking.service
                ).join(
                    User,
                    Service.users
                ).filter_by(
                    id=worker_id
                ).all()
            else:
                if customer_id:
                    result = Booking.query.filter_by(
                        customer_id=customer_id,
                        is_taken=False,
                        is_done=False,
                        is_cancel=False,
                        worker_id=None
                    ).all()
                else:
                    result = Booking.query.filter_by(
                        is_taken=False,
                        is_done=False,
                        is_cancel=False,
                        worker_id=None
                    ).all()
            return jsonify(BookingSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(BookingSchema(many=True).dump([]).data), 404


class BookingTakenApi(MethodView):
    def get(self):
        """get taken booking by service ids"""
        worker_id = request.args.get('worker_id', None)
        customer_id = request.args.get('customer_id', None)

        if worker_id and customer_id:
            return 'Either the worker_id and ' + \
                'customer_id should be provided', 400

        try:
            if worker_id:
                result = Booking.query.filter_by(
                    is_taken=True,
                    is_done=False,
                    is_cancel=False,
                    worker_id=worker_id
                ).all()
            else:
                if customer_id:
                    result = Booking.query.filter_by(
                        customer_id=customer_id,
                        is_taken=True,
                        is_done=False,
                        is_cancel=False,
                    ).all()
                else:
                    result = Booking.query.filter_by(
                        is_taken=True,
                        is_done=False,
                        is_cancel=False,
                    ).all()
            return jsonify(BookingSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(BookingSchema(many=True).dump([]).data), 404


class BookingIdApi(MethodView):
    def get(self, id):
        """get booking by id"""
        try:
            result = Booking.query.filter_by(id=id).one()
            return jsonify(BookingSchema(many=False).dump(result).data)
        except NoResultFound:
            return jsonify(BookingSchema(many=False).dump(None).data), 404

    def put(self, id):
        try:
            booking_date = datetime.datetime.strptime(request.form['booking_date'], "%m/%d/%Y").date() \
                if 'booking_date' in request.form else None
            booking_time = datetime.datetime.strptime(request.form['booking_time'], '%I:%M %p').time() \
                if 'booking_time' in request.form else None
            details = request.form['details'] \
                if 'details' in request.form else None
            address = request.form['address'] \
                if 'address' in request.form else None
            is_taken = request.form['is_taken'] \
                if 'is_taken' in request.form else None
            is_done = request.form['is_done'] \
                if 'is_done' in request.form else None
            is_cancel = request.form['is_cancel'] \
                if 'is_cancel' in request.form else None
        except Exception, ex:
            return "Could not validate booking information: {}". \
                format(repr(ex)), 400

        try:
            update_booking(
                id,
                booking_date,
                booking_time,
                details,
                address,
                is_taken,
                is_done,
                is_cancel
            )
        except Exception, ex:
            return "Error updating booking: {}". \
                format(repr(ex)), 400

        return jsonify(BookingSchema(many=True).dump(None).data), 200


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
        except NoResultFound:
            return "Booking request not found or already approved or rejected", 400
        except Exception, ex:
            return "Error approving booking request: {}". \
                format(repr(ex)), 400

        return jsonify(BookingRequestSchema(many=False).dump(None).data), 200


class BookingRequestIdRejectApi(MethodView):
    def put(self, id):
        """(customer) reject booking request"""
        try:
            reject_request(id)
        except NoResultFound:
            return "Booking request not found or already approved or rejected", 400
        except Exception, ex:
            return "Error rejecting booking request: {}". \
                format(repr(ex)), 400

        return jsonify(BookingRequestSchema(many=False).dump(None).data), 200


class CustomerIdBookingApi(MethodView):
    def get(self, id):
        """get bookings by customer id"""
        try:
            is_taken = request.args.get('is_taken', None)

            if is_taken is None:
                result = Booking.query.filter_by(customer_id=id).all()
            else:
                if is_taken:
                    result = Booking.query.filter_by(
                        customer_id=id,
                        is_taken=is_taken
                    ).all()
                else:
                    result = Booking.query.filter_by(
                        customer_id=id,
                        is_taken=is_taken,
                        worker_id=None
                    ).all()

            return jsonify(BookingSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(BookingSchema(many=True).dump([]).data), 404


class WorkerIdBookingApi(MethodView):
    def get(self, id):
        """get bookings by worker id"""
        try:
            is_taken = request.args.get('is_taken', 0)

            result = Booking.query.filter_by(
                worker_id=id,
                is_taken=is_taken
            ).all()
            return jsonify(BookingSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(BookingSchema(many=True).dump([]).data), 404


class WorkerBookingIdApproveApi(MethodView):
    def put(self, id):
        """approve a customer booking request by ID"""
        try:
            approve_customer_booking(id)
        except Exception, ex:
            return "Error approving customer booking request: {}". \
                format(repr(ex)), 400
