from flask import jsonify
from flask.views import MethodView
from models import Address
from schema import AddressSchema

class AddressApi(MethodView):
    def get(self, id):
        result = Address.query.filter_by(user_id=id).all()
        return jsonify(AddressSchema(many=True).dump(result).data)
