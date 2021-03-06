
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'yk'

urlpatterns = [
    path('', main, name='main'),
    path('join/start', join_start, name='join_start'),
    path('join/done', join_done, name='join_done'),
    path('join/1', join1, name='join1'),
    path('join/2', join2, name='join2'),
    path('join/3', join3, name='join3'),
    path('profile/<int:pk>', profile, name='profile'),
    path('my_profile', my_profile, name='my_profile'),
    path('friends', friends, name='friends'),
    path('friends/accept/<int:pk>', accept_friends, name='accept_friends'),
    path('friends/follow/<int:pk>', follow, name='follow'),
    path('location/', location, name='location'),
    path('ask/', ask, name='ask'),
    path('my_ask', my_ask, name='my_ask'),
    path('answer/', answer, name='answer'),
    path('report_user/<int:pk>', report_user, name='report_user'),
    path('report_ask/<int:pk>', report_ask, name='report_ask'),
]
