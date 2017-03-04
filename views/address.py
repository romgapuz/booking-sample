from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from models import Address

class AddressView(sqla.ModelView):
    column_labels = dict(user='Customer')

    column_searchable_list = (
        'address_type',
        'unit',
        'street',
        'city',
        'user.first_name',
        'user.last_name',
        'user.username',
        'user.email'
    )

    form_choices = {
        'city': [
            ('Caloocan', 'Caloocan'),
            ('Las Pinas', 'Las Pinas'),
            ('Makati', 'Makati'),
            ('Malabon', 'Malabon'),
            ('Mandaluyong', 'Mandaluyong'),
            ('Manila', 'Manila'),
            ('Marikina', 'Marikina'),
            ('Muntinlupa', 'Muntinlupa'),
            ('Navotas', 'Navotas'),
            ('Paranaque', 'Paranaque'),
            ('Pasay', 'Pasay'),
            ('Pasig', 'Pasig'),
            ('Quezon', 'Quezon'),
            ('San Juan', 'San Juan'),
            ('Taguig', 'Taguig'),
            ('Valenzuela', 'Valenzuela')
        ],
        'address_type': [
            ('Home', 'Home'),
            ('Work', 'Work'),
            ('Other', 'Other')
        ]
    }

    column_filters = (
        filters.FilterLike(
            Address.city,
            'City',
            options=(
                ('Caloocan', 'Caloocan'),
                ('Las Pinas', 'Las Pinas'),
                ('Makati', 'Makati'),
                ('Malabon', 'Malabon'),
                ('Mandaluyong', 'Mandaluyong'),
                ('Manila', 'Manila'),
                ('Marikina', 'Marikina'),
                ('Muntinlupa', 'Muntinlupa'),
                ('Navotas', 'Navotas'),
                ('Paranaque', 'Paranaque'),
                ('Pasay', 'Pasay'),
                ('Pasig', 'Pasig'),
                ('Quezon', 'Quezon'),
                ('San Juan', 'San Juan'),
                ('Taguig', 'Taguig'),
                ('Valenzuela', 'Valenzuela')
            )
        ),
        filters.FilterLike(
            Address.address_type,
            'Address Type',
            options=(
                ('Home', 'Home'),
                ('Work', 'Work'),
                ('Other', 'Other')
            )
        )
    )