from flask import jsonify
from flask.views import MethodView
from flask import request
from sqlalchemy.orm.exc import NoResultFound
from models.feedback import Feedback, add_feedback
from schema.feedback import FeedbackSchema
import datetime


def register(app):
    app.add_url_rule(
        '/customer/<id>/feedback',
        view_func=CustomerIdFeedbackApi.as_view('customer_id_feedback')
    )
    app.add_url_rule(
        '/worker/<id>/feedback',
        view_func=WorkerIdFeedbackApi.as_view('worker_id_feedback')
    )
    app.add_url_rule(
        '/feedback',
        view_func=FeedbackApi.as_view('user_id_feedback')
    )


class CustomerIdFeedbackApi(MethodView):
    def get(self, id):
        try:
            result = Feedback.query.filter_by(
                customer_id=id
            ).order_by(
                Feedback.feedback_date.desc()
            ).all()
            return jsonify(FeedbackSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(FeedbackSchema(many=True).dump([]).data), 404


class WorkerIdFeedbackApi(MethodView):
    def get(self, id):
        try:
            result = Feedback.query.filter_by(
                worker_id=id
            ).order_by(
                Feedback.feedback_date.desc()
            ).all()
            return jsonify(FeedbackSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(FeedbackSchema(many=True).dump([]).data), 404


class FeedbackApi(MethodView):
    def post(self):
        try:
            star = request.form['star']
            feedback_date = \
                datetime.datetime.strptime(
                    request.form['feedback_date'],
                    "%m/%d/%Y"
                ).date() \
                if 'worker_id' in request.form else \
                datetime.datetime.now().date()
            details = request.form['details']
            customer_id = request.form['customer_id']
            worker_id = request.form['worker_id']
        except Exception, ex:
            return "Could not validate feedback information: {}". \
                format(repr(ex)), 400

        try:
            add_feedback(
                star,
                feedback_date,
                details,
                customer_id,
                worker_id
            )
        except Exception, ex:
            return "Error creating feedback: {}". \
                format(repr(ex)), 400

        return jsonify(FeedbackSchema(many=False).dump(None).data), 201
