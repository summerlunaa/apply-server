from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'deadline',
        'body', 'image']