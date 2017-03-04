from flask_admin.contrib import sqla
from wtforms import validators
from models import (
    Service,
    User
)

class BookingView(sqla.ModelView):
    column_exclude_list = ['details']

    column_searchable_list = (
        'details',
        'customer.first_name',
        'customer.last_name',
        'customer.username',
        'customer.email',
        'worker.first_name',
        'worker.last_name',
        'worker.username',
        'worker.email'
    )

    form_args = dict(
        details=dict(validators=[validators.required()])
    )
    
    form_ajax_refs = {
        'customer': {
            'fields': (User.first_name, User.last_name, User.username, User.email)
        },
        'worker': {
            'fields': (User.first_name, User.last_name, User.username, User.email)
        },
        'service': {
            'fields': (Service.name,)
        }
    }