from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
class User(AbstractUser):
    avatar = CloudinaryField('avatar')
    follow = models.ManyToManyField("Follow", related_name='followers')

class Accommodation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='accommodation')
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Post(BaseModel):
    name = models.CharField(max_length=255)
    accommodation = models.OneToOneField(Accommodation,on_delete=models.CASCADE,related_name='post')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_user')
    content = models.TextField()
    def __str__(self):
        return self.name

class Media(models.Model):
    name = models.CharField(max_length=255)
    image = CloudinaryField('image')
    updated_at = models.DateTimeField(auto_now=True,null=True)
    media_accommodation = models.ForeignKey(Accommodation,on_delete=models.CASCADE,related_name='media_accommodation')


class Comment(BaseModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment_post')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comment')
    content = models.CharField(max_length=255)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set', related_query_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set', related_query_name='followers')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Notification(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    def __str__(self):
        return self.name