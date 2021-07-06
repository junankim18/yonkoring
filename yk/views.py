from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User


def main(request):
    user = request.user
    ctx = {
        'user': user
    }
    return render(request, 'main.html', ctx)


def join_start(request):
    user = request.user
    ctx = {
        'user': user
    }
    return render(request, 'join_start.html', ctx)


def join1(request):
    user = request.user
    if request.method == 'GET':
        try:
            if Profile.objects.get(user=user):
                pass
        except:
            new_profile = Profile()
            new_profile.user = request.user
            new_profile.save()

        ctx = {
            'user': user
        }
        return render(request, 'join1.html', ctx)
    elif request.method == 'POST':
        block_school = request.POST['block_school']
        if block_school == 'block':
            block_school = True
        else:
            block_school = False

        my_profile = Profile.objects.get(user=user)
        my_profile.profile_image = request.FILES['image']
        my_profile.phone_number = request.POST['phone_number']
        my_profile.school = request.POST['school']
        my_profile.block_school = block_school
        my_profile.age = request.POST['age']
        my_profile.mbti = request.POST['mbti']
        my_profile.gender = request.POST['gender']
        my_profile.bio = request.POST['bio']

        my_profile.save()

        ctx = {
            'user': user
        }
        return render(request, 'join2.html', ctx)


def join2(request):
    user = request.user
    if request.method == 'GET':
        ctx = {
            'user': user
        }
        return render(request, 'join2.html', ctx)
    elif request.method == 'POST':
        my_profile = Profile.objects.get(user=user)
        my_profile.goal = request.POST['goal']
        my_profile.major = request.POST['major']

        my_profile.save()

        ctx = {
            'user': user
        }
        return render(request, 'join3.html', ctx)


def join3(request):
    user = request.user
    if request.method == 'GET':
        ctx = {
            'user': user
        }
        return render(request, 'join3.html', ctx)
    elif request.method == 'POST':
        interest_list = request.POST['interest']
        interest_num = len(interest_list.split('#'))
        for i in range(interest_num):
            globals()["new_interest{}".format(i)] = Interest()
            globals()["new_interest{}".format(
                i)].interest = interest_list.split('#')[i]
            globals()["new_interest{}".format(i)].save()

        my_profile = Profile.objects.get(user=user)
        my_profile.club = request.POST['club']
        for i in range(interest_num):
            my_profile.interest.add(globals()["new_interest{}".format(i)])
        my_profile.save()

        ctx = {
            'user': user
        }
        return render(request, 'join_done.html', ctx)


def join_done(request):
    user = request.user
    ctx = {
        'user': user
    }
    return render(request, 'join_done.html', ctx)


def social_login(request):
    user = request.user
    ctx = {
        'user': user
    }
    return render(request, 'login.html', ctx)


def profile(request, pk):
    user = User.objects.get(id=pk)
    profile = Profile.objects.get(user=user)
    asks = list(Ask.objects.filter(ask_to=user))
    for ask in asks:
        if len(ask.ask.all()) == 0:
            asks.remove(ask)
    ctx = {
        'user': user,
        'profile': profile,
        'asks': asks
    }
    return render(request, 'profile.html', ctx)


def my_profile(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    asks = list(Ask.objects.filter(ask_to=user))
    ctx = {
        'user': user,
        'profile': profile,
        'asks': asks
    }
    return render(request, 'my_profile.html', ctx)


def ask(request, pk):
    ctx = {

    }
    return render(request, 'ask.html', ctx)
