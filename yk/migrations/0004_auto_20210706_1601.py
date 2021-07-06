# Generated by Django 3.2.5 on 2021-07-06 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yk', '0003_auto_20210705_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='block_school',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='학교 안보이기'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=150, null=True, verbose_name='친구 신청 메시지')),
                ('message_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_from', to=settings.AUTH_USER_MODEL)),
                ('message_report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_report', to=settings.AUTH_USER_MODEL)),
                ('message_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
