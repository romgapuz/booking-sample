from flask import Flask
import api.user as api_user
import api.feedback as api_feedback
import api.service as api_service
import api.booking as api_booking
from schema.base import ma
from models.base import db
import admin
from utils.config import read_config

# read config
config = read_config()

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = config.get('app', 'secret_key')

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = \
    config.get('db', 'sqlalchemy_database_uri')
app.config['SQLALCHEMY_ECHO'] = \
    True if config.get('db', 'sqlalchemy_echo') == 'True' else False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = \
    True if \
    config.get('db', 'sqlalchemy_track_modifications') == 'True' \
    else False
db.app = app
db.init_app(app)

# Schema
ma.app = app
ma.init_app(app)

# api and admin registration
api_user.register(app)
api_feedback.register(app)
api_service.register(app)
api_booking.register(app)
admin.register(app, db)


# start app
if __name__ == '__main__':
    app.run(debug=True)
