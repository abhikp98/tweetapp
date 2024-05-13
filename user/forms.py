
from typing import Any, Mapping
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from user.models import Posts, UserProfile


class Register(UserCreationForm):
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Password"}),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Re enter Password"}),
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets={
            'username': forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            'first_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"}),
            'last_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            # 'password1': forms.TextInput(attrs={"class": "form-control"}),
            # 'password2': forms.TextInput(attrs={"class": "form-control"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Enter username",
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Username',
                   'label': ""
                   }
            )
        )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'
                ,
                "placeholder": "Password",
                "label": ""
                   }
            )
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    


class UpdateProfile(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets={
            "bio": forms.TextInput(attrs={"class": "form-control w-50 mx-auto"}),
            "avatar": forms.FileInput(attrs={"class": "form-control w-50 mx-auto"})
        }


class CreateTweet(ModelForm):
    class Meta:
        model = Posts
        fields = ['tweet']
        widgets = {
            "tweet": forms.Textarea(attrs={"class": "form-control", "rows": "3", "placeholder": "Shoot Your Thouts Here!"})
        }



