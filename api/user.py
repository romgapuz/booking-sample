from flask import jsonify
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound
from models.user import User
from schema.user import UserSchema


def register(app):
    app.add_url_rule(
        '/user/',
        view_func=UserApi.as_view('user'))
    app.add_url_rule(
        '/user/<id>',
        view_func=UserApiId.as_view('user_id')
    )


class UserApi(MethodView):
    def get(self):
        result = User.query.all()
        return jsonify(UserSchema(many=True).dump(result).data)


class UserApiId(MethodView):
    def get(self, id):
        try:
            result = User.query.filter_by(id=id).one()
            return jsonify(UserSchema(many=False).dump(result).data)
        except NoResultFound:
            return jsonify(UserSchema(many=True).dump(None).data), 404
