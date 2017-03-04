from flask import jsonify
from flask.views import MethodView
from models import Service, User
from schema import ServiceSchema

class ServiceApi(MethodView):
    def get(self):
        result = Service.query.order_by(Service.name).all()
        return jsonify(ServiceSchema(many=True).dump(result).data)

class UserServiceApi(MethodView):
    def get(self, id):
        result = Service.query.join(User.services, Service).all()
        print result #.filter_by(User.services.user_id=id)
        #Service.query.join(User.services.any(id=id)).all()
        return jsonify(ServiceSchema(many=True).dump(result).data)
