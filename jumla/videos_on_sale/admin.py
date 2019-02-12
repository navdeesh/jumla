from django.apps import apps
from django.contrib import admin

# Register your models here.
from .models import Users

admin.site.register(Users)
app_models = apps.get_app_config('videos_on_sale').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass