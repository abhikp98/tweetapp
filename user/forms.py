
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from user.models import Posts, UserProfile


class Register(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets={
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'password1': forms.PasswordInput(attrs={"class": "form-control"}),
            'password2': forms.PasswordInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Enter username",
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Username'
                   }
            )
        )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'
                ,
                "placeholder": "Password"
                   }
            )
        )
    


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



