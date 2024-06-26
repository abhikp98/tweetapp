"""
URL configuration for tweetapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path

from user import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('feeds/', views.FeedView.as_view(), name="feeds"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('like/<slug>/', views.addLike.as_view(), name="like"),
    path('<slug>/tweet-view/', views.Tweetview.as_view(), name="viewtweet"),
    path('<slug>/delete-tweet/', views.DeleteTweet.as_view(), name='delete-tweet'),
    path('followers/', views.FollowersView.as_view(), name="followers"),
    path('users/<userid>/', views.ViewFollower.as_view(), name="user-profile"),
    path('FollowUnfollow/<userid>', views.FollowUnfollow.as_view(), name="connect"),
]
