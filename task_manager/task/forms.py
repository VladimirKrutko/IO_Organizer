from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UpdateTeamUserForm(forms.Form):
    user = forms.CharField(max_length=100)


class CreateTeamForm(forms.Form):
    name = forms.CharField(max_length=100)
    user = forms.CharField(max_length=100)


class CreateTaskForm(forms.Form):
    STATUS_CHOICES = (
        ('D', 'Done'),
        ('F', 'Femme'),
        ('S', 'Stop'))
    executor = forms.CharField(max_length=100)
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    end_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    TEAM_CHOICES = [(obj[0], obj[0]) for obj in Team.objects.values_list('name')]
    team = forms.ChoiceField(choices = TEAM_CHOICES)


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['executor', 'status', 'content', 'end_data']
        label = {
            'executor_id': 'executor',
            'end_data': 'end_date',
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)
