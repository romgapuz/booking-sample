from flask import jsonify
from flask.views import MethodView
from models.address import Address
from schema.address import AddressSchema


def register(app):
    app.add_url_rule(
        '/user/<id>/address',
        view_func=UserIdAddressApi.as_view('user_id_address')
    )


class UserIdAddressApi(MethodView):
    def get(self, id):
        result = Address.query.filter_by(user_id=id).all()
        return jsonify(AddressSchema(many=True).dump(result).data)

    def post(self, id):
        try:
            address_type = request.form['address_type']
            unit = request.form['unit']
            street = request.form['street']
            city = request.form['city']

            address_id = add_address(
                id,
                address_type,
                unit,
                street,
                city
            )

            return '{}'.format(address_id), 201
        except Exception, ex:
            return "Add address failed: {}".format(repr(ex)), 400
