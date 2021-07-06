# Generated by Django 3.2.5 on 2021-07-05 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yk', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='ask',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='report',
        ),
        migrations.AddField(
            model_name='profile',
            name='mbti',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='mbti'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_report',
            field=models.ManyToManyField(blank=True, related_name='user_report', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Ask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=100, null=True, verbose_name='question')),
                ('ask_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ask_from', to=settings.AUTH_USER_MODEL)),
                ('ask_report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ask_report', to=settings.AUTH_USER_MODEL)),
                ('ask_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ask_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True, null=True, verbose_name='answer')),
                ('ask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ask', to='yk.ask')),
            ],
        ),
    ]