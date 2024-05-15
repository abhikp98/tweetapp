from msilib.schema import ListView
from tkinter import NO
from urllib import request
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView, CreateView, ListView, View, UpdateView, DetailView, DeleteView
from .models import UserProfile
from user.models import Posts
from .forms import CreateTweet, Register, LoginForm, UpdateProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if self.request.user.is_authenticated:
            return redirect('feeds')
        return super().get(request, *args, **kwargs)
    template_name = "index.html"


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    success_url = reverse_lazy('feeds')

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        print("yes")
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            usr = authenticate(self.request, username=uname, password=pwd)
            if usr:
                login(request, usr)
                return redirect('feeds')
        messages.error(request,"Username or Password is Incorrect!")
        return render(request,self.template_name,{"form":form})


class RegisterView(CreateView):
    form_class = Register
    template_name = "register.html"
    model = User
    success_url = reverse_lazy('feeds')
    
    def form_valid(self, form):
        valid = super().form_valid(form)
        usr = authenticate(self.request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
        login(self.request, usr)
        UserProfile.objects.create(user=self.request.user)
        return valid

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request,"failed to create account")
        return super().form_invalid(form)
    

class FeedView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "login"
    model = Posts
    template_name = "feed.html"
    success_url = reverse_lazy('feeds')
    form_class = CreateTweet
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print("came here", form.cleaned_data.get('tweet'))
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        if search:
            self.request.session['search'] = search
            context['posts'] = Posts.objects.filter(user__in=[i for i in UserProfile.objects.get(user=self.request.user).followers.all()]).filter(user__username__icontains=search)
        else:
            self.request.session.delete('search')
            print("came hereee")
            context['posts'] = Posts.objects.filter(user__in=[i for i in UserProfile.objects.get(user=self.request.user).followers.all()])
        return context
    

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    

class ProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    success_url = reverse_lazy('profile')
    login_url = '/login/'
    redirect_field_name = 'login'
    form_class = UpdateProfile
    template_name = "update-profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Posts.objects.filter(user=self.request.user)
        uc = 0
        for i in UserProfile.objects.all():
            if self.request.user in i.followers.all():
                uc += 1
        context['followerscount'] = uc
        return context

    def get_object(self, queryset=None):
        return self.request.user.userprofile
    


class addLike(LoginRequiredMixin, DetailView):
    login_url = "/login/"
    redirect_field_name = "login"
    model = Posts
    def get(self, request, *args, **kwargs):
        qry = Posts.objects.get(slug__contains=kwargs.get("slug"))
        if qry.likes.filter(id=request.user.id).exists():
            print("yes")
            qry.likes.remove(request.user)
        else:
            print("no")
            qry.likes.add(request.user)
        return redirect(self.request.META.get('HTTP_REFERER', '/feeds'))
    

class Tweetview(LoginRequiredMixin, DetailView):
    login_url = "/login/"
    redirect_field_name = "login"
    model = Posts
    template_name = "tweet-details.html"


class DeleteTweet(LoginRequiredMixin, DeleteView):
    login_url = "/login/"
    redirect_field_name = "login"
    model = Posts
    template_name = "delete-tweet.html"
    success_url = reverse_lazy('profile')


class FollowersView(LoginRequiredMixin, DetailView):
    login_url = "/login/"
    redirect_field_name = "login"
    model = UserProfile
    template_name = "followers.html"

    def get_object(self, queryset=None):
        return self.request.user.userprofile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        if search is not None:
            context['follow'] = User.objects.filter(username__icontains=search).exclude(id=self.request.user.id).exclude(is_superuser=True)
        return context
    

class ViewFollower(LoginRequiredMixin, DetailView):
    login_url = "/login/"
    redirect_field_name = "login"
    model = UserProfile
    template_name = "follower-profile.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Posts.objects.filter(user__username=self.kwargs.get("userid"))
        uc = 0
        for i in UserProfile.objects.all():
            if self.object.user in i.followers.all():
                uc += 1
        context['followerscount'] = uc
        return context

    def get_object(self, queryset=None):
        userprofile = UserProfile.objects.get(user__username=self.kwargs.get("userid"))
        return userprofile
    


class FollowUnfollow(LoginRequiredMixin, DetailView):
    login_url = "/login/"
    redirect_field_name = "login"
    model = UserProfile
    def get(self, request, *args, **kwargs):
        userid = User.objects.get(username=kwargs.get('userid'))
        qry = UserProfile.objects.get(id=request.user.id)
        if  qry.followers.filter(id=userid.id).exists():
            qry.followers.remove(userid)
        else:
            qry.followers.add(userid)
        return redirect(self.request.META.get('HTTP_REFERER', '/feeds'))
