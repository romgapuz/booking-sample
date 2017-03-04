from schema import ma
from models import Address

class AddressSchema(ma.ModelSchema):
    class Meta:
        model = Address