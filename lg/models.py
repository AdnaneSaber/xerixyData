from django.contrib.auth.models import User
from django.db import models


class Cities(models.Model):
    name = models.CharField(max_length=64,default="Casablanca")

    def __str__(self) -> str:
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/', default='avatars/default.png')

    def __str__(self) -> str:
        return self.user.username


class ArticleCategories(models.Model):
    name = models.CharField(max_length=255, default="NaN")

    def __str__(self) -> str:
        return self.name


class Articles(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    price = models.IntegerField()
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ArticleCategories, on_delete=models.CASCADE)
    boughts = models.IntegerField(default=0, blank=True)
    avatar = models.ImageField(
        upload_to='article/', default='article/default.jpeg')

    def __str__(self) -> str:
        return self.name
