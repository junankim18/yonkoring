from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Interest(models.Model):
    interest = models.CharField(verbose_name='관심사', max_length=50)

    def __str__(self):
        return self.interest


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='profile_images', blank=True, null=True)
    phone_number = models.IntegerField(
        verbose_name='전화번호', blank=True, null=True)
    nickname = models.CharField(
        verbose_name='닉네임', max_length=20, blank=True, null=True)
    school = models.CharField(
        verbose_name='학교', max_length=20, blank=True, null=True)
    block_school = models.BooleanField(
        verbose_name='학교 안보이기', default=False, blank=True, null=True)
    age = models.IntegerField(verbose_name='나이', blank=True, null=True)
    gender = models.CharField(
        verbose_name='성별', max_length=20, blank=True, null=True)
    goal = models.CharField(
        verbose_name='목표', max_length=100, blank=True, null=True)
    major = models.CharField(
        verbose_name='전공', max_length=50, blank=True, null=True)
    bio = models.TextField(verbose_name='자기 소개', blank=True, null=True)
    mbti = models.CharField(verbose_name='mbti',
                            max_length=50, blank=True, null=True)
    interest = models.ManyToManyField(
        Interest, related_name='interests', blank=True)
    club = models.CharField(
        verbose_name='동아리', max_length=150, blank=True, null=True)
    user_report = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='user_report', blank=True)
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='following', blank=True)
    follower = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='follower', blank=True)
    today_friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='today_friends', blank=True)
    yesterday_friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='yesterday_friends', blank=True)

    def __str__(self):
        return self.user.username


class Ask(models.Model):
    question = models.CharField(
        verbose_name='question', max_length=100, blank=True, null=True)
    ask_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='ask_to', on_delete=models.CASCADE)
    ask_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='ask_from', on_delete=models.CASCADE)
    ask_report = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='ask_report', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.TextField(verbose_name='answer', blank=True, null=True)
    ask = models.ForeignKey(Ask, related_name='ask', on_delete=models.CASCADE)
    answered_at = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.answer


class Message(models.Model):
    message = models.CharField(
        verbose_name='친구 신청 메시지', max_length=150, blank=True, null=True)
    message_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='message_to', on_delete=models.CASCADE)
    message_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='message_from', on_delete=models.CASCADE)
    message_report = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='message_report', on_delete=models.CASCADE, blank=True, null=True)
