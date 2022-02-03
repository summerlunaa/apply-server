from unicodedata import name
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.forms.models import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError


class UserSignupForm(forms.Form):

    name = forms.CharField(label="이름(실명)", required=True, max_length=15)
    email = forms.EmailField(label="이메일", required=True)
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="비밀번호 재확인", widget=forms.PasswordInput, required=True)
    major = forms.CharField(label="전공 / 복수(연계)전공", required=True, max_length=30)
    phone_number = forms.CharField(label="연락처", required=True, max_length=13)
    student_id = forms.CharField(label="학번", required=True, max_length=9)
    class Meta:
         model = CustomUser
         fields = ['name',  'email', 'password1', 'password2', 'major', 'phone_number', 'student_id']

    def clean_email(self):
        email = self.cleaned_data['email']
        try: CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError("해당 이메일로 가입한 유저가 이미 존재합니다.")

    def clean_phonenum(self):
        phone_number = self.cleaned_data['phone_number']
        try: CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return phone_number
        raise ValidationError("해당 번호로 가입한 유저가 이미 존재합니다.")

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 맞지 않습니다.")
        try: validate_password(password2, user=CustomUser)
        except ValidationError: 
            raise ValidationError("비밀번호는 8자 이상이며 숫자만으로 구성하면 안됩니다.")
        return password2

    def save(self):
        # 이메일, 패스워드 확인 후 저장.
        email = self.clean_email()
        password = self.clean_password2()
        name = self.cleaned_data['name']
        major = self.cleaned_data['major']
        phone_number = self.cleaned_data['phone_number']
        student_id = self.cleaned_data['student_id']
        user = CustomUser.objects.create_user(email, password, False, name, -1, major, phone_number, student_id)
        return user


class KakaoForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'student_id', 'major']