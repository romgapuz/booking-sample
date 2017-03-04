from schema import ma
from models import Feedback

class FeedbackSchema(ma.ModelSchema):
    class Meta:
        model = Feedback