from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import AddUserForm

# Create your views here.
MENU = ['Tasks', 'Settings', 'Profile', 'Sign in', 'Sign out']


def index(request):
    return render(request, 'task/base.html', {'menu': MENU})


def register_request(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect("/home")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})
    return render(request=request, template_name="task/register.html", context={"register_form": form, 'menu': MENU})

    # return render(request=request, template_name="task/register.html", context={"register_form": form, 'menu': MENU})
