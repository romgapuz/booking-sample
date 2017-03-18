from flask import jsonify
from flask.views import MethodView
from flask import request
from sqlalchemy.orm.exc import NoResultFound
from models.user import User, add_customer, update_customer
from schema.user import UserSchema


def register(app):
    app.add_url_rule(
        '/user/',
        view_func=UserApi.as_view('user'))
    app.add_url_rule(
        '/user/<id>',
        view_func=UserIdApi.as_view('user_id')
    )
    app.add_url_rule(
        '/login',
        view_func=LoginApi.as_view('login')
    )
    app.add_url_rule(
        '/register',
        view_func=RegisterApi.as_view('register')
    )


class UserApi(MethodView):
    def get(self):
        try:
            result = User.query.all()
            return jsonify(UserSchema(many=True).dump(result).data)
        except NoResultFound:
            return jsonify(UserSchema(many=True).dump([]).data), 404


class UserIdApi(MethodView):
    def get(self, id):
        try:
            result = User.query.filter_by(id=id).one()
            return jsonify(UserSchema(many=False).dump(result).data)
        except NoResultFound:
            return jsonify(UserSchema(many=True).dump(None).data), 404

    def put(self, id):
        try:
            first_name = request.form['first_name'] \
                if 'first_name' in request.form else None
            last_name = request.form['last_name'] \
                if 'last_name' in request.form else None
            username = request.form['username'] \
                if 'username' in request.form else None
            password = request.form['password'] \
                if 'password' in request.form else None
            email = request.form['email'] \
                if 'email' in request.form else None
        except Exception, ex:
            return "Could not validate user information: {}". \
                format(repr(ex)), 400

        try:
            update_customer(
                id,
                first_name,
                last_name,
                username,
                password,
                email
            )
        except Exception, ex:
            return "Error updating user: {}". \
                format(repr(ex)), 400

        return jsonify(UserSchema(many=True).dump(None).data), 200


class LoginApi(MethodView):
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


class RegisterApi(MethodView):
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
