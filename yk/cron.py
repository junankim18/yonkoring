from .models import *
from django.contrib.auth.models import User, AnonymousUser


def every1am():
    user = User.objects.get(id=1)
    profile = Profile.objects.get(user=user)
    profile.interest.add('test')
    profile.save()
