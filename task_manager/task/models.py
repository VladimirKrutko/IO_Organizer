from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, username, email, password, role='user'):
        user = self.model(username=username, email=email, role=role)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password, 'admin')
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model in innoter project
    """

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self) -> models.EmailField:
        return self.email


class Team(models.Model):
    teaam_id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100)
    user_id = models.ManyToManyField(User)


class Task(models.Model):
    task_id = models.IntegerField(primary_key=True, auto_created=True)
    end_data = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    executor = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id) + '_' + str(self.page_id)
