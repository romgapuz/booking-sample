from schema import ma
from models import Booking

class BookingSchema(ma.ModelSchema):
    class Meta:
        model = Booking