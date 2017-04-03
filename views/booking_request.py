from flask_admin.contrib import sqla
from wtforms import validators
from models.user import User


class BookingRequestView(sqla.ModelView):
    column_exclude_list = ['details']

    column_searchable_list = (
        'details',
        'booking.service_name',
        'worker.first_name',
        'worker.last_name',
        'worker.username',
        'worker.email'
    )

    form_args = dict(
        details=dict(validators=[validators.required()])
    )

    form_ajax_refs = {
        'worker': {
            'fields': (
                User.first_name,
                User.last_name,
                User.username,
                User.email
            )
        }
    }

    form_choices = {
        'status': [
            ('1', 'Pending'),
            ('2', 'Approved'),
            ('3', 'Rejected')
        ]
    }
