from django.db import models

# Create your models here.

class User(models.Model):

    name = models.CharField(max_length=256)
    nickname = models.CharField(max_length=64)


class Theme(models.Model):
    name = models.CharField(max_length=256)
    user = models.ManyToManyField(User)
    is_padoru = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
