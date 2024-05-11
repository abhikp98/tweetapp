from operator import mod
from random import randint
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

class UserProfile(models.Model):
    bio = models.CharField(max_length=50, default="Hey There!")
    avatar = models.ImageField(upload_to="media", default="/media/defaultprofile.jpg")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="followers", null=True, blank=True)

    def __str__(self) -> str:
        return self.user.first_name


class Posts(models.Model):
    tweet = models.CharField(max_length=200)
    slug = models.SlugField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def save(self, **kwrgs):
        uname = self.tweet[:20]
        print(uname, "check")
        if Posts.objects.filter(slug=slugify(uname)).exists():
            extra = str(randint(1, 10000))
            print("yes model")
            self.slug = slugify(uname) + "-" + extra
        else:
            print("no model")
            self.slug = slugify(uname)
        return super().save()

    def __str__(self) -> str:
        return self.tweet
    

    def likes_count(self):
        return self.likes.count()
