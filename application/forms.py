from django import forms
from .models import Application
from user.models import CustomUser


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'portfolio', 'design_doc']


class UserPositionForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['position']