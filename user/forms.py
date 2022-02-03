from select import select
from turtle import position
from unicodedata import name
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.forms.models import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError


class UserSignupForm(forms.Form):
    position_choices=[
        (None, '선택'),
        ('개발', '개발'),
        ('기획', '기획'),
        ('디자인', '디자인'),
    ]
    name = forms.CharField(label="이름(실명)", required=True, max_length=15)
    email = forms.EmailField(label="이메일", required=True)
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="비밀번호 재확인", widget=forms.PasswordInput, required=True)
    major = forms.CharField(label="전공 / 복수(연계)전공", required=True, max_length=30)
    phone_number = forms.CharField(label="연락처", required=True, max_length=13)
    student_id = forms.CharField(label="학번", required=True, max_length=9)
    position = forms.ChoiceField(label="내가 선택한 포지션은 ", choices=position_choices, required=True)
    
    class Meta:
         model = CustomUser
         fields = ['name',  'email', 'password1', 'password2', 'major', 'phone_number', 'student_id', 'position']
    
    def not_default_position(self):
        print(self.cleaned_data.get('position'))
        try : self.cleaned_data.get('position')
        except KeyError:
            raise ValidationError("개발/기획/디자인 중 포지션을 선택해주세요!")
        return self.cleaned_data['position']

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
        position = self.not_default_position()
        user = CustomUser.objects.create_user(email, password, False, name, -1, major, phone_number, student_id, position)
        return user


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Login Email", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def check_is_active(self, user):
        return user.is_active

    def authenticate_login(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise ValueError("Email or Password is not exact.")
            else:
                if self.check_is_active(user):
                    return True
                else:
                    return False
        else:
            raise ValueError("Email and Password should be filled(not empty).")


class KakaoForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'student_id', 'major']

class Emailform(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'phone_number', 'student_id', 'major']
