from flask import jsonify
from flask.views import MethodView
from flask import request
from sqlalchemy.orm.exc import NoResultFound
from models.user import User, add_customer, update_customer
from schema.user import UserSchema
from utils.email_sender import EmailSender


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
        '/customer/login',
        view_func=CustomerLoginApi.as_view('customer_login')
    )
    app.add_url_rule(
        '/customer/<id>/verify',
        view_func=CustomerIdVerifyApi.as_view('customer_id_verify')
    )
    app.add_url_rule(
        '/worker/login',
        view_func=WorkerLoginApi.as_view('worker_login')
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
            return jsonify(UserSchema(many=False).dump(None).data), 404

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
            phone_no = request.form['phone_no'] \
                if 'phone_no' in request.form else None
            is_verified = request.form['is_verified'] \
                if 'is_verified' in request.form else None
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
                email,
                phone_no,
                is_verified
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
            user = User.query.filter_by(
                username=username,
                is_verified=True
            ).one()

            if user.password != password:
                return "Incorrect password", 403
        except Exception:
            return "Username not found or verified", 403

        return str(user.id)


class CustomerLoginApi(MethodView):
    def post(self):
        try:
            username = request.form['username']
            password = request.form['password']
        except Exception, ex:
            return "Could not validate username and password: {}". \
                format(repr(ex)), 400

        try:
            user = User.query.filter_by(
                username=username,
                role='Customer',
                is_verified=True
            ).one()

            if user.password != password:
                return "Incorrect password", 403
        except Exception:
            return "User not found", 403

        return str(user.id)


class CustomerIdVerifyApi(MethodView):
    def post(self, id):
        try:
            item = User.query.filter_by(
                id=id,
                role='Customer',
                is_verified=False,
            ).one()
        except Exception, ex:
            return "Customer not found or already verified: {}". \
                format(repr(ex)), 400
    
        try:
            es = EmailSender()
            es.send_verification(item.id, item.email, item.first_name)
        except Exception, ex:
            return "Sending email failed: {}". \
                format(repr(ex)), 500

        return "Verification email sent"

    def get(self, id):
        try:
            item = User.query.filter_by(
                id=id,
                role='Customer',
                is_verified=False
            ).one()
        except Exception:
            return "Customer not found or already verified", 403

        try:
            update_customer(
                id,
                None,
                None,
                None,
                None,
                None,
                None,
                True
            )
        except Exception, ex:
            return "Error verifying customer: {}". \
                format(repr(ex)), 500

        return "Customer verified successfully"


class WorkerLoginApi(MethodView):
    def post(self):
        try:
            username = request.form['username']
            password = request.form['password']
        except Exception, ex:
            return "Could not validate username and password: {}". \
                format(repr(ex)), 400

        try:
            user = User.query.filter_by(
                username=username,
                role='Worker'
            ).one()

            if user.password != password:
                return "Incorrect password", 403
        except Exception:
            return "User not found", 403

        return str(user.id)


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
