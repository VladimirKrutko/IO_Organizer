from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['content', 'executor', 'status']
        widgets = {
            'executor': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)
