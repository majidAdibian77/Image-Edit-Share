from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userProfileInfo")
    bio = models.TextField(max_length=100, blank=True, default="Bio")
    profile_pic = models.ImageField(upload_to='profile_users', default="server_images/profileUser.png", blank=True)
    typeOfUser = models.TextField(max_length=20, default="simple")
    score = models.IntegerField(default=10)

    def __str__(self):
        return self.user.username


class PostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", unique=False)
    image = models.ImageField(upload_to='user_images', blank=True)
    text = models.TextField(max_length=100, blank=True, default="")
    score = models.IntegerField(default=0)
    post_time = models.DateTimeField(default=datetime.now, blank=True)
    approved = models.BooleanField(default=False)

    def set_post_time(self):
        self.post_time = datetime.now()
        self.save()

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.user.username


class Users_give_score(models.Model):
    post = models.ForeignKey(PostModel, related_name="users_give_score", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CommentPostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(verbose_name="Text")
    comment_time = models.DateTimeField(default=datetime.now)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text
