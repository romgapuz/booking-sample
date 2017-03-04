from schema import ma
from models import Message

class MessageSchema(ma.ModelSchema):
    class Meta:
        model = Message