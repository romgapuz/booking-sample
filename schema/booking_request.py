from schema.base import ma
from models.booking_request import BookingRequest


class BookingRequestSchema(ma.ModelSchema):
    class Meta:
        model = BookingRequest
