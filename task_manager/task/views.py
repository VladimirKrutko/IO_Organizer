from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect
from .forms import UserCreationForm, CreateTaskForm
from  .models import Task

MENU = ['Tasks', 'Settings', 'Profile', 'Sign in', 'Sign out']


def index(request):
    return render(request, 'task/base.html', {'menu': MENU})


class TaskView(View):
    template_name = 'task/create_task.html'

    def get(self, request):
        context = {
            'form': CreateTaskForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CreateTaskForm(request.POST)
        Task(form.data['content'], form.data['executor'], form.data['status']).save()
        if form.is_valid():

            form.save()
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
