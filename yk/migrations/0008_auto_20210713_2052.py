# Generated by Django 3.2.5 on 2021-07-13 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yk', '0007_auto_20210707_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='latitude',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='위도'),
        ),
        migrations.AddField(
            model_name='profile',
            name='logitude',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='경도'),
        ),
    ]