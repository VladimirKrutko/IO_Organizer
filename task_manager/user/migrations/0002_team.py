# Generated by Django 4.1.5 on 2023-01-03 05:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('teaam_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('user_id', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
