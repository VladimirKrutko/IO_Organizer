from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('task', TemplateView.as_view(template_name='task/task.html'), name='task'),
    path('', TemplateView.as_view(template_name='task/home.html'), name='home'),
    path('users/', include('task.urls')),
]
