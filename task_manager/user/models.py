from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
import jwt
from datetime import datetime, timedelta
from django.conf import settings


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
# docker run --name some-postgres -e POSTGRES_PASSWORD=postgres -d postgres

class User(AbstractBaseUser, PermissionsMixin):
    """
    User model in innoter project
    """

    class Roles(models.TextChoices):
        """
        Class with user roles
        """
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200)
    role = models.CharField(max_length=9, choices=Roles.choices, default='user')
    create_data = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self) -> models.EmailField:
        return self.email

    # @property
    # def token(self):
    #     return self._generate_jwt_token()
    #
    # def get_role(self) -> models.CharField:
    #     return self.role
    #
    # def _generate_jwt_token(self):
    #     dt = datetime.now() + timedelta(days=30)
    #
    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')
    #
    #     return token


class UploadImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=name, blank=True, null=True)
