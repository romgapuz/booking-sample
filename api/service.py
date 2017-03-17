from flask import jsonify
from flask.views import MethodView
from sqlalchemy.orm import subqueryload
from sqlalchemy.orm.exc import NoResultFound
from models.service import Service
from models.user import User
from schema.service import ServiceSchema


def register(app):
    app.add_url_rule(
        '/service',
        view_func=ServiceApi.as_view('service')
    )
    app.add_url_rule(
        '/user/<id>/service',
        view_func=UserServiceApi.as_view('user_id_service')
    )


class ServiceApi(MethodView):
    def get(self):
        result = Service.query.order_by(Service.name).all()
        return jsonify(ServiceSchema(many=True).dump(result).data)


class UserServiceApi(MethodView):
    def get(self, id):
        try:
            result = User.query.options(
                subqueryload(User.services)
            ).filter_by(id=id).one()
            return jsonify(ServiceSchema(many=True).dump(result.services).data)
        except NoResultFound:
            return jsonify(ServiceSchema(many=True).dump([]).data), 404
