# Register your models here.
from django.contrib import admin
from django.apps import apps
from Trainer.models import *

# Get current app config
app = apps.get_app_config('Trainer')  # replace with your app name

# Loop through all models in the app and register them
for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass  # skip if already registered
