from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Team(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.ManyToManyField(User)


class Task(models.Model):
    STATUS_CHOICES = (
        ('D', 'Done'),
        ('P', 'Femme'),
        ('S', 'Stop'))
    end_data = models.DateField(default=timezone.now)
    content = models.TextField()
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now_add=True)
    executor = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    team = models.ForeignKey(Team, default=-1, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.id)
