from flask import jsonify
from flask.views import MethodView
from models.feedback import Feedback
from schema.feedback import FeedbackSchema


def register(app):
    app.add_url_rule(
        '/user/<id>/feedback',
        view_func=FeedbackApi.as_view('user_id_feedback')
    )


class FeedbackApi(MethodView):
    def get(self, id):
        result = Feedback.query \
            .filter_by(user_id=id) \
            .order_by(Feedback.feedback_date.desc()) \
            .all()
        return jsonify(FeedbackSchema(many=True).dump(result).data)
