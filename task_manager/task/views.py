from django.shortcuts import render

# Create your views here.
MENU = ['Tasks', 'Settings', 'Profile', 'Sign in', 'Sign out']


def index(request):
    return render(request, 'task/index.html', {'menu': MENU})
