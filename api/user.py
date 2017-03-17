from flask import jsonify
from flask.views import MethodView
from flask import request
from sqlalchemy.orm.exc import NoResultFound
from models.user import User, add_customer
from schema.user import UserSchema


def register(app):
    app.add_url_rule(
        '/user/',
        view_func=UserApi.as_view('user'))
    app.add_url_rule(
        '/user/<id>',
        view_func=UserApiId.as_view('user_id')
    )
    app.add_url_rule(
        '/login',
        view_func=Login.as_view('login')
    )
    app.add_url_rule(
        '/register',
        view_func=Register.as_view('register')
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


class Login(MethodView):
    def post(self):
        try:
            username = request.form['username']
            password = request.form['password']
        except Exception, ex:
            return "Could not validate username and password: {}". \
                format(repr(ex)), 400

        try:
            user = User.query.filter_by(username=username).one()

            if user.password != password:
                return "Incorrect password", 403
        except Exception:
            return "Username not found", 403

        return "Login successful"


class Register(MethodView):
    def post(self):
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            user_id = add_customer(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email=email
            )

            return '{}'.format(user_id), 201
        except Exception, ex:
            return "Registration failed: {}".format(repr(ex)), 400
