
from django.contrib import admin
from django.urls import path, include, register_converter

import uuid

from chat.views import *

app_name= "chat"

class UUIDConverter:
    regex = '[0-9a-f-]+'

    def to_python(self, value):
        return uuid.UUID(value)

    def to_url(self, value):
        return str(value)

register_converter(UUIDConverter, 'uuid')


urlpatterns = [
    path("user_list/", user_list, name= "user_list"),
    
    path("user_profiles/", user_profiles, name= "user_profiles"),
    
    path('room/<uuid:user_id>/', room, name='room'),
    
]