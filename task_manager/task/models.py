from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()


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
