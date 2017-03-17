from flask import jsonify
from flask.views import MethodView
from sqlalchemy.orm import subqueryload
from sqlalchemy.orm.exc import NoResultFound
from models.service import Service
from models.user import User
from schema.service import ServiceSchema
from schema.user import UserSchema


def register(app):
    app.add_url_rule(
        '/service',
        view_func=ServiceApi.as_view('service')
    )
    app.add_url_rule(
        '/user/<id>/service',
        view_func=UserServiceApi.as_view('user_id_service')
    )
    app.add_url_rule(
        '/service/<id>/worker',
        view_func=ServiceIdWorkerApi.as_view('service_id_worker')
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


class ServiceIdWorkerApi(MethodView):
    def get(self, id):
        try:
            result = User.query.filter(
                User.services.any(id=id)
            ).filter_by(role='Worker').all()
            return jsonify(UserSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(UserSchema(many=True).dump([]).data), 404
