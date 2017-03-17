from schema.base import ma
from models.feedback import Feedback


class FeedbackSchema(ma.ModelSchema):
    class Meta:
        model = Feedback
