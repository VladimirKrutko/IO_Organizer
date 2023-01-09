from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect
from .forms import CreateTaskForm, UserRegistrationForm, UpdateTaskForm
from .models import Task, User
from datetime import datetime

MENU = ['Tasks', 'Settings', 'Profile', 'Sign in', 'Sign out']


def index(request):
    return render(request, 'task/base.html', {'menu': MENU})


def delete_task(request, pk):
    Task.objects.filter(id=pk).delete()
    return redirect('task')


class UpdateTaskView(View):
    template_name = 'task/create_task.html'

    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        context = {
            'form': UpdateTaskForm(instance=task)
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        form = UpdateTaskForm(instance=task)
        if form.is_valid():
            executor = form.cleaned_data.get('executor')
            end_date = form.cleaned_data.get('end_date')
            user = User.objects.filter(email=executor)[0]
            Task(content=form.cleaned_data.get('content'), executor=user, status=form.cleaned_data.get('status'),
                 end_data=datetime.strptime(end_date, '%m/%d/%y %H:%M')).save()
            return redirect('task')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = UpdateTaskForm(instance=task)
    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, instance=task)
        executor = form.cleaned_data.get('executor')
        end_date = form.cleaned_data.get('end_date')
        user = User.objects.filter(email=executor)[0]
        Task(content=form.cleaned_data.get('content'), executor=user, status=form.cleaned_data.get('status'),
             end_data=datetime.strptime(end_date, '%m/%d/%y %H:%M')).save()
        return redirect('task')
    return redirect('home')


def get_user_task(request):
    tasks = [task.__dict__ for task in Task.objects.filter(executor=request.user)]
    for i in tasks:
        i['executor'] = request.user.email

    return render(request, 'task/task.html', {'data': tasks})


class TaskView(View):
    template_name = 'task/create_task.html'

    def get(self, request):
        context = {
            'form': CreateTaskForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            executor = form.cleaned_data.get('executor')
            end_date = form.cleaned_data.get('end_date')
            user = User.objects.filter(email=executor)[0]
            Task(content=form.cleaned_data.get('content'), executor=user, status=form.cleaned_data.get('status'),
                 end_data=datetime.strptime(end_date, '%m/%d/%y %H:%M')).save()
            return redirect('task')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserRegistrationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserRegistrationForm(request.POST)

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
