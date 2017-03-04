import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from wtforms import validators

import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters

from models import (
    db,
    Service,
    User,
    Booking,
    Address,
    Feedback,
    Message
)
from views import (
    UserView,
    BookingView,
    AddressView,
    FeedbackView
)
from api import (
    UserApi,
    UserApiId,
    AddressApi,
    FeedbackApi,
    ServiceApi,
    UserServiceApi
)
from schema import ma

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = 'd6550c610e95438e8e302d4b312b0a5e'

# Create in-memory database
app.config['DATABASE_FILE'] = 'ekonek.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

# Schema
ma.app = app
ma.init_app(app)

# API
app.add_url_rule('/user/', view_func=UserApi.as_view('user'))
app.add_url_rule('/user/<id>', view_func=UserApiId.as_view('user_id'))
app.add_url_rule('/user/<id>/address', view_func=AddressApi.as_view('user_id_address'))
app.add_url_rule('/user/<id>/feedback', view_func=FeedbackApi.as_view('user_id_feedback'))
app.add_url_rule('/service', view_func=ServiceApi.as_view('service'))
app.add_url_rule('/user/<id>/service', view_func=UserServiceApi.as_view('user_id_service'))

# Create admin
admin = admin.Admin(app, name='eKonek', template_mode='bootstrap3')

# Add views
admin.add_view(UserView(User, db.session))
admin.add_view(BookingView(Booking, db.session))
admin.add_view(AddressView(Address, db.session))
admin.add_view(FeedbackView(Feedback, db.session))
admin.add_view(sqla.ModelView(Message, db.session))
admin.add_view(sqla.ModelView(Service, db.session))

def build_sample_db():
    db.drop_all()
    db.create_all()

    # create services
    service_list = []
    for tmp in ["Beauticians", "Carpenters", "ComputerTechnicians", "Electricians", "Gardeners", "Laborers", "Masseuses", "Painters", "Plumbers", "Therapists"]:
        service = Service()
        service.name = tmp
        service_list.append(service)
        db.session.add(service)

    db.session.commit()
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)
