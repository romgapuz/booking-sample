from schema.base import ma
from models.service import Service


class ServiceSchema(ma.ModelSchema):
    class Meta:
        model = Service

        exclude = ['service']
