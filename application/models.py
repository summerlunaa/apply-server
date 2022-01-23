from django.db import models
from django.utils import timezone
from user.models import CustomUser


class Question(models.Model):
    object = models.Manager()
    number = models.PositiveIntegerField()
    content = models.TextField(default='')
    limit = models.PositiveIntegerField()

    def __str__(self):
        return self.number


class Answer(models.Model):
    object = models.Manager()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class Portfolio(models.Model):
    object = models.Manager()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(null=True, blank=True)