from flask import Flask
import api.user as api_user
import api.feedback as api_feedback
import api.service as api_service
import api.booking as api_booking
from schema.base import ma
from models.base import db
import admin

# Create application
app = Flask(__name__)

# configure database
app.config.from_pyfile('config.py')
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
    app.run(debug=True, threaded=True)
