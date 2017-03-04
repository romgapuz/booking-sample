from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters

class FeedbackView(sqla.ModelView):
    column_labels = dict(user='Worker')

    column_searchable_list = (
        'feedback_date',
        'details',
        'user.first_name',
        'user.last_name',
        'user.username',
        'user.email'
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