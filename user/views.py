from msilib.schema import ListView
from urllib import request
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView, CreateView, ListView, View
from .models import UserProfile

import user
from user.models import Posts
from .forms import Register, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class IndexView(TemplateView):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if self.request.user.is_authenticated:
            print("yes")
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
        messages.error(request,"invalid credentail")
        return render(request,self.template_name,{"form":form})


        return super().post(request, *args, **kwargs)



class RegisterView(CreateView):
    form_class = Register
    template_name = "register.html"
    model = User
    success_url = reverse_lazy('feeds')
    def get_context_data(self, **kwargs):
        usr = authenticate(self.request, username=self.kwargs.get('username'), password=self.kwargs.get('password1'))
        login(self.request, usr)
        return super().get_context_data(**kwargs)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request,"failed to create account")
        return super().form_invalid(form)
    

class FeedView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "login"
    model = Posts
    template_name = "feed.html"
    def get_queryset(self):
        search = self.request.GET.get("q")
        qs = super().get_queryset().exclude(user=self.request.user)
        if search:
           return qs.filter(user__first_name__icontains=search)
        return qs
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usr = UserProfile.objects.filter(user=self.request.user)
        if usr.exists():
            context['propic'] = usr[0].avatar
        else:
            context['propic'] = ""
        return context
    


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
