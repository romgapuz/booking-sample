from flask_admin.contrib import sqla


class FeedbackView(sqla.ModelView):
    column_labels = dict(user='Worker')

    column_searchable_list = (
        'feedback_date',
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

    form_choices = {
        'star': [
            ('1', 'One'),
            ('2', 'Two'),
            ('3', 'Three'),
            ('4', 'Four'),
            ('5', 'Five')
        ]
    }
