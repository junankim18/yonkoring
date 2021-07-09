import random
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, AnonymousUser


def main(request):
    admin = User.objects.get(id=1)
    user_list = list(User.objects.all())
    try:
        if User.objects.get(user=request.user):
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
        for i in range(1, interest_num):
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
    admin = User.objects.get(id=1)
    profile = Profile.objects.get(user=user)
    asks = list(Ask.objects.filter(ask_to=user))
    user_list = list(User.objects.all())
    user_list.remove(user)
    user_list.remove(request.user)
    user_list.remove(admin)
    random_user = random.choice(user_list)

    for ask in asks:
        if len(ask.ask.all()) == 0:
            asks.remove(ask)

    ctx = {
        'user': user,
        'profile': profile,
        'asks': asks,
        'random_user': random_user
    }
    return render(request, 'profile.html', ctx)


def my_profile(request):
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
    user = request.user
    friend = User.objects.get(id=pk)
    if request.method == 'GET':
        ctx = {
            'friend': friend,
            'user': user
        }
        return render(request, 'ask.html', ctx)
    elif request.method == 'POST':
        new_ask = Ask()
        new_ask.question = request.POST['question']
        new_ask.ask_to = friend
        new_ask.ask_from = user
        new_ask.save()
        ctx = {
            'friend': friend,
            'user': user
        }
        return redirect('/profile/'+str(friend.id))


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
