import flask_admin as admin
from flask_admin.contrib import sqla
from views.user import UserView
from views.booking import BookingView
from views.booking_request import BookingRequestView
from views.feedback import FeedbackView
from views.service import ServiceView
from models.service import Service
from models.user import User
from models.booking import Booking
from models.booking_request import BookingRequest
from models.feedback import Feedback
from models.reset_password import ResetPassword


def register(app, db):
    # create admin
    admin_view = admin.Admin(app, name='eKonek', template_mode='bootstrap3')

    # add views
    admin_view.add_view(UserView(User, db.session))
    admin_view.add_view(BookingView(Booking, db.session))
    admin_view.add_view(BookingRequestView(BookingRequest, db.session))
    admin_view.add_view(FeedbackView(Feedback, db.session))
    admin_view.add_view(ServiceView(Service, db.session))
    admin_view.add_view(sqla.ModelView(ResetPassword, db.session))
