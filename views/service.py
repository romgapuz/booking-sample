from flask_admin.contrib import sqla


class ServiceView(sqla.ModelView):
    column_searchable_list = (
        'name',
    )
