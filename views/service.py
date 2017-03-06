from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters

class ServiceView(sqla.ModelView):
    column_searchable_list = (
        'name',
    )