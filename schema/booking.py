from schema.base import ma
from models.booking import Booking


class BookingSchema(ma.ModelSchema):
    class Meta:
        model = Booking
