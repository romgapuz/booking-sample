from schema.base import ma
from models.message import Message


class MessageSchema(ma.ModelSchema):
    class Meta:
        model = Message
