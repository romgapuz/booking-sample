from schema import ma
from models import Service

class ServiceSchema(ma.ModelSchema):
    class Meta:
        model = Service

        exclude = ['service']