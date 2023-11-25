from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from models import strg


class CustomView(ModelView):
    def __init__(self, model, **kwargs):
        super(CustomView, self).__init__(model, strg.session, **kwargs)
    # Override the create_model method to customize the create view
    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        return super(CustomView, self).create_view()

    def create_model(self, form):
        obj = self.model(**form.data)
        return obj

    def on_model_change(self, form, model, is_created):
        # Customize what happens on model change (both create and update)
        pass