from django.db import models

# Create your models here.


class User(models.Model):
    class UserType(models.IntegerChoices):
        USER = 1
        PROMOTER = 2

    username = models.CharField(max_length=128, unique=True, primary_key=True)
    user_type = models.IntegerField(choices=UserType.choices)
    state = models.IntegerField()


class Paper(models.Model):
    author_username = models.CharField(max_length=128)
    promoter_username = models.CharField(max_length=128)
    file = models.FileField()
    title = models.CharField(max_length=512)
    isAccepted = models.BooleanField(default=False)
