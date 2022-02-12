from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.forms.models import ModelForm
from django.shortcuts import render
from httpx import request
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


class UserSignupForm(forms.Form):
    email = forms.EmailField(label="이메일", required=True)
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="비밀번호 재확인", widget=forms.PasswordInput, required=True)
 
    class Meta:
         model = CustomUser
         fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        try: CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError("해당 이메일로 가입한 유저가 이미 존재합니다.")

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
        password = self.clean_password2()  # email,  password, is_kakao, name, kakao_id, major, phone_number, student_id, position
        user = CustomUser.objects.create_user(email, password, False, 'name', -1, 'major', 'phone_number', 'student_id', 'position')
        return user


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label="이메일", required=True)
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput)

    def check_is_active(self, user):
        return user.is_active

    def authenticate_login(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                return None
            else:
                if self.check_is_active(user):
                    return True
                else:
                    return False
        else:
            raise ValueError("Email and Password should be filled(not empty).")

class Emailform(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'phone_number', 'student_id', 'major', 'position']
