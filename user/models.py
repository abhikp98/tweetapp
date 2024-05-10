from random import randint
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

class UserProfile(models.Model):
    bio = models.CharField(max_length=50, default="Hey There!")
    avatar = models.ImageField(upload_to="media", default="/media/defaultprofile.jpg")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    def save(self, force_insert, force_update, using, update_fields):
        uname = self.tweet[:20]
        if Posts.objects.filter(slug=uname).exists():
            extra = str(randint(1, 10000))
            self.slug = slugify(uname) + "-" + extra
        else:
            self.slug = slugify(uname)
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        return self.tweet
