# Generated by Django 3.2.5 on 2021-07-06 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yk', '0004_auto_20210706_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='answeres_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
