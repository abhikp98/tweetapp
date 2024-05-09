from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    bio = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="profile")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="followers")

    def __str__(self) -> str:
        return self.user.first_name


class Posts(models.Model):
    tweet = models.CharField(max_length=200)
    slug = models.SlugField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.tweet