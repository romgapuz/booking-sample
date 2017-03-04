from flask import jsonify
from flask.views import MethodView
from models import Feedback
from schema import FeedbackSchema

class FeedbackApi(MethodView):
    def get(self, id):
        result = Feedback.query \
            .filter_by(user_id=id) \
            .order_by(Feedback.feedback_date.desc()) \
            .all()
        return jsonify(FeedbackSchema(many=True).dump(result).data)
