from celery import Celery
from celery.schedules import crontab
import schedule
import time
import threading
import requests
from urllib.parse import urlparse
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import random
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, AnonymousUser
import json


def main(request):
    admin = User.objects.get(id=1)
    user_list = list(User.objects.all())
    try:
        user_list.remove(request.user)
    except:
        pass
    user_list.remove(admin)
    random_user = random.choice(user_list)

    user = request.user
    ctx = {
        'user': user,
        'random_user': random_user,
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
        try:
            block_school = request.POST['block_school']
            if block_school == 'block':
                block_school = True
        except:
            block_school = False

        my_profile = Profile.objects.get(user=user)
        my_profile.profile_image = request.FILES['image']
        my_profile.phone_number = request.POST['onlyNumber']
        my_profile.school = request.POST['school']
        my_profile.block_school = block_school
        my_profile.age = request.POST['age']
        my_profile.mbti = request.POST['mbti']
        my_profile.gender = request.POST['gender']
        my_profile.bio = request.POST['introduce']

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
        my_profile.goal = request.POST['introduce']
        my_profile.major = request.POST['self_info']

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
        interest_list = request.POST['self_info']
        interest_num = len(interest_list.split('#'))
        for i in range(1, interest_num):
            globals()["new_interest{}".format(i)] = Interest()
            globals()["new_interest{}".format(
                i)].interest = interest_list.split('#')[i]
            globals()["new_interest{}".format(i)].save()

        my_profile = Profile.objects.get(user=user)
        my_profile.club = request.POST['introduce']
        for i in range(1, interest_num):
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

    friend = User.objects.get(id=pk)
    admin = User.objects.get(id=1)
    user_list = list(User.objects.all())
    user_list.remove(friend)
    try:
        user_list.remove(request.user)
    except:
        pass
    user_list.remove(admin)

    random_user = random.choice(user_list)

    friend_profile = Profile.objects.get(user=friend)

    asks_whole = list(Ask.objects.filter(ask_to=friend))
    ask_mine = list(Ask.objects.filter(ask_to=friend, ask_from=request.user))
    asks = []
    for i in range(len(asks_whole)):
        if len(asks_whole[i].ask.all()) != 0 and asks[i].ask_report == None:
            asks.append(asks_whole[i])
    for i in range(len(ask_mine)):
        asks.append(ask_mine[i])

    ctx = {
        'friend': friend,
        'friend_profile': friend_profile,
        'asks': asks,
        'random_user': random_user
    }
    return render(request, 'profile.html', ctx)


def my_ask(request):
    asks = list(Ask.objects.filter(ask_to=request.user))
    my_ask = []
    for i in range(len(asks)):
        if len(asks[i].ask.all()) == 0 and asks[i].ask_report == None:
            my_ask.append(asks[i])
    ctx = {
        'my_ask': my_ask
    }
    return render(request, 'my_ask.html', ctx)


def my_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    asks = list(Ask.objects.filter(ask_to=user, ask_report=None))
    ctx = {
        'user': user,
        'profile': profile,
        'asks': asks
    }
    return render(request, 'my_profile.html', ctx)


@ csrf_exempt
def ask(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        friend_id = req['id']
        question = req['question']
        friend = User.objects.get(id=friend_id)
        new_ask = Ask()
        new_ask.question = question
        new_ask.ask_to = friend
        new_ask.ask_from = request.user
        new_ask.save()
        return JsonResponse({'friend_id': friend_id, 'question': question})


@ csrf_exempt
def answer(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        ask_id = req['id']
        answer = req['answer']
        this_ask = Ask.objects.get(id=ask_id)
        new_answer = Answer()
        new_answer.ask = this_ask
        new_answer.answer = answer
        new_answer.save()
        return JsonResponse({'ask_id': ask_id, 'answer': answer})


def friends(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    followings = profile.following.all()
    following_list = []
    for following in followings:
        following_list.append(Profile.objects.get(user=following))

    followers = profile.follower.all()
    follower_list = []
    for follower in followers:
        follower_list.append(Profile.objects.get(user=follower))

    today_friends = profile.today_friends.all()
    today_friends_list = []
    for today_friend in today_friends:
        today_friends_list.append(Profile.objects.get(user=today_friend))

    yesterday_friends = profile.yesterday_friends.all()
    yesterday_friends_list = []
    for yesterday_friend in yesterday_friends:
        yesterday_friends_list.append(
            Profile.objects.get(user=yesterday_friend))

    ctx = {
        'user': user,
        'profile': profile,
        'following_list': following_list,
        'follower_list': follower_list,
        'today_friends_list': today_friends_list,
        'yesterday_friends_list': yesterday_friends_list,
    }
    return render(request, 'friends.html', ctx)


def accept_friends(request, pk):
    user = request.user
    friend = User.objects.get(id=pk)

    profile = Profile.objects.get(user=user)
    profile.today_friends.add(friend)
    profile.follower.remove(friend)
    profile.save()

    followings = profile.following.all()
    following_list = []
    for following in followings:
        following_list.append(Profile.objects.get(user=following))

    followers = profile.follower.all()
    follower_list = []
    for follower in followers:
        follower_list.append(Profile.objects.get(user=follower))

    today_friends = profile.today_friends.all()
    today_friends_list = []
    for today_friend in today_friends:
        today_friends_list.append(Profile.objects.get(user=today_friend))

    yesterday_friends = profile.yesterday_friends.all()
    yesterday_friends_list = []
    for yesterday_friend in yesterday_friends:
        yesterday_friends_list.append(
            Profile.objects.get(user=yesterday_friend))

    ctx = {
        'user': user,
        'profile': profile,
        'following_list': following_list,
        'follower_list': follower_list,
        'today_friends_list': today_friends_list,
        'yesterday_friends_list': yesterday_friends_list,

    }
    return render(request, 'friends.html', ctx)


def follow(request, pk):
    user = request.user
    friend = User.objects.get(id=pk)
    friend_profile = Profile.objects.get(user=friend)
    friend_profile.follower.add(user)
    friend_profile.save()
    return redirect('/profile/'+str(friend.id))


@ csrf_exempt
def location(request):
    req = json.loads(request.body)
    latitude = req['latitude']
    longitude = req['longitude']
    address = req['address']
    user = request.user
    profile = Profile.objects.get(user=user)
    profile.latitude = latitude
    profile.longitude = longitude
    profile.address = address
    profile.save()
    return JsonResponse({'latitude': latitude, 'longitude': longitude, 'address': address})


def report_user(request, pk):
    friend = User.objects.get(id=pk)
    friend_profile = Profile.objects.get(user=friend)
    friend_profile.user_report.add(request.user)
    friend_profile.save()
    return redirect('/')


def report_ask(request, pk):
    ask = Ask.objects.get(id=pk)
    ask.ask_report = request.user
    ask.save()
    return redirect('/')


def printhello():
    print('hello')


schedule.every().day.at('21:09').do(printhello)
