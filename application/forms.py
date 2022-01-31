from django import forms
from .models import Answer, Portfolio


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['file']