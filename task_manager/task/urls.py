from django.urls import path, include

from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register', Register.as_view(), name='register'),
    path('create_task', TaskView.as_view(), name='create_task'),
    path('create_team', CreateTeamView.as_view(), name='create_team'),
    path('show_task', get_user_task, name='task'),
    path('show_team', get_team_info, name='team'),
    path('add_user/<int:pk>/', AddUserTeamView.as_view(), name='add_user'),
    # path('task/<int:id>/', TaskView.as_view(), name='task'),
    path('update_task/<int:pk>/', UpdateTaskView.as_view(), name='update_task'),
    path('delete_task/<int:pk>/', delete_task, name='delete_task'),



]
