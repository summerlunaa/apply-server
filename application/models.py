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
    portfolio = models.FileField(null=True, blank=True, upload_to='portfolio')
    design_doc = models.FileField(null=True, blank=True, upload_to='design_doc')
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        solve = self.user.position +'-'+ self.user.name
        return solve
