from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path("register", register_request, name="register")
]
