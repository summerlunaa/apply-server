from django.db import models
from django.utils import timezone
from user.models import CustomUser


class Application(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer1 = models.TextField(default='', blank=True)
    answer2 = models.TextField(default='', blank=True)
    answer3 = models.TextField(default='', blank=True)
    answer4 = models.TextField(default='', blank=True)
    answer5 = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__():
        return user


class Portfolio(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(null=True, blank=True)

    def __str__():
        return user