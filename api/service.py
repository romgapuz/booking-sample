from flask import jsonify
from flask.views import MethodView
from sqlalchemy.orm import subqueryload
from sqlalchemy.orm.exc import NoResultFound
from models import Service, User
from schema import ServiceSchema

class ServiceApi(MethodView):
    def get(self):
        result = Service.query.order_by(Service.name).all()
        return jsonify(ServiceSchema(many=True).dump(result).data)

class UserServiceApi(MethodView):
    def get(self, id):
        response_body = None
        try:
            result = User.query.options(subqueryload(User.services)).filter_by(id=id).one()
            return jsonify(ServiceSchema(many=True).dump(result.services).data)
        except NoResultFound:
            return jsonify(ServiceSchema(many=True).dump([]).data), 404
