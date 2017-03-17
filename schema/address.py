from schema.base import ma
from models.address import Address


class AddressSchema(ma.ModelSchema):
    class Meta:
        model = Address
