from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

# Create your models here.
User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    profile_img = models.ImageField(upload_to='profile_images', default='blank_image.jpg')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    username = models.CharField(max_length=50)
    image = models.ImageField(upload_to='post_images')
    caption = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.username
    
class Likes(models.Model):
    post_id = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    
class FollowerCount(models.Model):
    follower = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user