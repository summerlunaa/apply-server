from django import forms
from .models import Application
from user.models import CustomUser
from django.core.exceptions import ValidationError


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'portfolio', 'design_doc']

    def empty_error(self):
        return ("채워지지 않은 항목이 있습니다.")


class UserPositionForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['position']