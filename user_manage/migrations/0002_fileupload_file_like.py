# Generated by Django 3.2.3 on 2021-10-26 06:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_manage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='file_like',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
