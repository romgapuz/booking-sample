from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from models import (
    User,
    Service
)

class UserView(sqla.ModelView):
    column_exclude_list = ['username', 'password']

    column_searchable_list = (
        'first_name',
        'last_name',
        'username',
        'email',
        'role',
        'services.name'
    )

    column_filters = (
        'services',
        filters.FilterLike(
            User.role,
            'Role',
            options=(
                ('Worker', 'Worker'),
                ('Customer', 'Customer')
            )
        )
    )

    form_excluded_columns = ['bookings', 'addresses', 'feedbacks']

    form_choices = {
        'role': [
            ('Worker', 'Worker'),
            ('Customer', 'Customer')
        ]
    }

    form_ajax_refs = {
        'services': {
            'fields': (Service.name,)
        }
    }