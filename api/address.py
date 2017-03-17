from flask import jsonify
from flask.views import MethodView
from models.address import Address
from schema.address import AddressSchema


def register(app):
    app.add_url_rule(
        '/user/<id>/address',
        view_func=AddressApi.as_view('user_id_address')
    )


class AddressApi(MethodView):
    def get(self, id):
        result = Address.query.filter_by(user_id=id).all()
        return jsonify(AddressSchema(many=True).dump(result).data)
