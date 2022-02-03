from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, resolve_url
from django.core.mail.message import EmailMessage
from django.conf import settings
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import *
import requests


def success(request) :
    """
    로그인, 회원가입 성공 시 돌아가 페이지로 향하는 view
    """
    return render(request, 'success.html') 


def login_home(request):
    """
    로그인, 회원가입을 진행할 페이지로 향하는 view
    """
    return render(request, 'login_home.html')


def signup_email(request):
    """
    일반(이메일) 회원가입 처리해주는 view
    이메일 회원가입 완료 후 로그인 페이지로 향함
    """ 
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='user.kakaobackends.KakaoBackend') #authenticate
            return redirect('login_home')
        else : 
            print(form)
            print("Invalid Form")
            print(form.errors)
            return render(request, 'signup_email.html',{'form':form})
    else:
        form = UserSignupForm()
    return render(request, 'signup_email.html', {'form':form})


def email_login(request):
    """
    일반(이메일) 회원가입 처리해주는 view
    로그인 완료 후 로그인 성공 시 이동할 페이지로 향함 (상의 필요)
    """
    if request.method=="POST":
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            if form.authenticate_login():
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user, backend='user.kakaobackends.KakaoBackend') 
                    return redirect('success')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'email_login.html', {'form':form})


def kakao_login(request):
    """
    
    """
    if request.user.is_authenticated:
        raise Exception("User already logged in")
    rest_api_key = settings.KAKAO_REST_API_KEY
    redirect_uri = "http://127.0.0.1:8000/user/kakao/login/callback/"
    state = "none"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={redirect_uri}&response_type=code&state={state}")


def submit_kakao(request):
    if not request.user.is_authenticated:
        raise ValidationError("잘못된 접근입니다(Not authenticated)")
    form = KakaoForm(request.POST, instance=request.user)
    if request.method=="POST":
        form = KakaoForm(request.POST, instance=request.user)
        print("form is post")
        if form.is_valid():
            print("form valid")
            form.save()
            return redirect('success')
    else:
        print("else")
    return render(request, 'submit_kakao.html', {'form':form})


def kakao_login_callback(request):
    """
    1) 인가코드 받기 -> redirect uri 인가 코드가 리다이렉트될 URI
    2) access_token 받기 -> 카카오 서버상 로그인 완료
    3-1) 카카오 첫 로그인일 경우 회원가입/로그인 진행 
    => 카카오로부터 사용자 정보 받기 (name (필수), email(옵션))
    => 추가 정보 받을 HTML로 이동시키기 (이메일, 학번, 전공, 전화번호)
    3-2) 카카오 로그인 했던 사람인 경우, 바로 로그인 진행
    4) 회원가입/로그인 완료 후 이동할 HTML로 넘어가기
    """
    code = request.GET.get("code")
    if code is None:
        raise Exception("code is none")

    state = request.GET.get("state") 
    token_url = "https://kauth.kakao.com/oauth/token"
    rest_api_key = settings.KAKAO_REST_API_KEY
    redirect_uri = "http://127.0.0.1:8000/user/kakao/login/callback/"
    res = requests.post(token_url, data={'grant_type':'authorization_code', 'client_id':rest_api_key, 'redirect_uri':redirect_uri, 'code':code}) 
    token_response = res.json()
    access_token = token_response.get('access_token')
    info_url = "https://kapi.kakao.com/v2/user/me"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'secure_resource': True}
    info_res = requests.get(info_url, headers=headers, params=params)

    try:
        info = info_res.json()
    except:
        info = None
    kakao_id = str(info.get("id"))

    try :
        test = CustomUser.objects.get(kakao_id=kakao_id)
    except CustomUser.DoesNotExist:
        test = None

    if  test is None: 
        personal_info = info.get("kakao_account")
        agree_on_nickname = personal_info.get("profile_needs_agreement")
        if not agree_on_nickname :
            profile = personal_info.get("profile")
            name = profile.get("nickname")
            print(name)
        agree_on_email = personal_info.get("email_needs_agreement")

        if not agree_on_email: 
            email = personal_info.get("email")
            print(email)
        else:
            email = ''
        major = "본전공 / 복수전공"
        phone_number = "010-****-****"
        student_id = "20******"
        user = CustomUser.objects.create_user(email, None, True, name, kakao_id, major, phone_number, student_id)
        form = KakaoForm()                   #email, password, is_kakao, name, kakao_id , major, phone_number, student_id
        login(request, user, backend='user.kakaobackends.KakaoBackend')
        return render(request, 'submit_kakao.html', {'form':form})

    else:
        login(request, CustomUser.objects.get(kakao_id=kakao_id), backend='user.kakaobackends.KakaoBackend')
        if state=="none":
            return redirect('success') #TO-DO : 우선은 로그인 완료 후 임시 페이지로 이동하게 함
        else:
            return redirect('success')


def logout_view(request):
    """
    로그아웃 처리
    1) 카카오로그인 경우 - 이 서비스에서만 로그아웃
    2) 일반 로그인 경우
    => 로그아웃 완료 후 우선은 login_home으로 돌아가게 해놓음, 상의 필요
    """
    if request.user.is_kakao:
        kakao_admin_key = settings.KAKAO_ADNIN_KEY 
        logout_url = "https://kapi.kakao.com/v1/user/logout"
        target_id = request.user.kakao_id
        target_id = int(target_id)
        headers = {'Authorization': f'KakaoAK {kakao_admin_key}'}
        data = {'target_id_type':'user_id','target_id':target_id}
        logout_res = requests.post(logout_url, headers=headers, data=data).json()
        response = logout_res.get("id")
        if target_id != response:
            return Exception('Kakao Logout failed')
        else:
            print(str(response) + "Kakao Logout successed")
    logout(request)
    return redirect('login_home')


def logout_with_kakao(request):
    """
    카카오톡과 함께 로그아웃 처리
    """
    kakao_rest_api_key = settings.KAKAO_REST_API_KEY
    logout_redirect_uri = "http://127.0.0.1:8000/user/logout/"
    state = "none" 
    kakao_service_logout_url = "https://kauth.kakao.com/oauth/logout"
    return redirect(f"{kakao_service_logout_url}?client_id={kakao_rest_api_key}&logout_redirect_uri={logout_redirect_uri}&state={state}")


def delete_user(request, user_pk):
    """
    탈퇴하기
    """
    user =request.user
    if user.pk == user_pk:
        if user.is_kakao:
            kakao_admin_key = settings.KAKAO_ADNIN_KEY
            user_kakao_id = int(user.kakao_id) 
            url = "https://kapi.kakao.com/v1/user/unlink"
            headers = {'Authorization':f'KakaoAK {kakao_admin_key}'} 
            data = {'target_id_type':'user_id','target_id': user_kakao_id}
            res = requests.post(url, headers=headers, data=data)
            deleted_user_id = res.json().get("id")
            if deleted_user_id == user_kakao_id:
                print("연결 끊기 성공")
            else:
                print("연결끊기 실패")
        logout(request)
        user.delete()
        return redirect('login_home')
    else:
        raise ValidationError("잘못된 접근입니다.")


def send_email(request):
    subject = "message"
    to = ["junior0614@naver.com"]
    from_email = "kdyme0614@gmail.com"
    message = "왜 안뒈~~~~~"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url=reverse_lazy('password_reset_complete')
    template_name = 'password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context
