from schema.base import ma
from models.user import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
