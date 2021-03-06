# Generated by Django 3.2.5 on 2021-07-07 12:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yk', '0006_rename_answeres_at_answer_answered_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='today_friends',
            field=models.ManyToManyField(blank=True, related_name='today_friends', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='yesterday_friends',
            field=models.ManyToManyField(blank=True, related_name='yesterday_friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
