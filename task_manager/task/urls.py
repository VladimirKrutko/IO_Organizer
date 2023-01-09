from django.urls import path, include

from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register', Register.as_view(), name='register'),
    path('create_task', TaskView.as_view(), name='create_task'),
    path('show_task', get_user_task, name='task'),
    path('task/<int:id>/', TaskView.as_view(), name='task')
]
