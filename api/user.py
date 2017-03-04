from flask import jsonify
from flask.views import MethodView
from models import User
from schema import UserSchema

class UserApi(MethodView):
    def get(self):
        result = User.query.all()
        return jsonify(UserSchema(many=True).dump(result).data)


class UserApiId(MethodView):
    def get(self, id):
        result = User.query.filter_by(id=id).one()
        return jsonify(UserSchema(many=False).dump(result).data)
