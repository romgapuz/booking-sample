import os
import os.path as op
from flask import Flask
import api.user as api_user
import api.address as api_address
import api.feedback as api_feedback
import api.service as api_service
from schema.base import ma
from models.base import db
import admin

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = 'd6550c610e95438e8e302d4b312b0a5e'

# Create in-memory database
app.config['DATABASE_FILE'] = 'ekonek.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

# Schema
ma.app = app
ma.init_app(app)

# api and admin registration
api_user.register(app)
api_address.register(app)
api_feedback.register(app)
api_service.register(app)
admin.register(app, db)


def build_sample_db():
    from models.service import Service

    db.drop_all()
    db.create_all()

    # create services
    service_list = []
    for tmp in [
            "Beauticians",
            "Carpenters",
            "ComputerTechnicians",
            "Electricians",
            "Gardeners",
            "Laborers",
            "Masseuses",
            "Painters",
            "Plumbers",
            "Therapists"]:
        service = Service()
        service.name = tmp
        service_list.append(service)
        db.session.add(service)

    db.session.commit()
    return


if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)
