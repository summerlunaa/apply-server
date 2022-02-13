from django.conf import settings

from django.contrib.auth.forms import (
    PasswordResetForm,
)

from django.contrib.auth.tokens import default_token_generator

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, resolve_url
from django.conf import settings
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import SetPasswordForm
from .forms import *
import requests


def success(request):
    """
    로그인, 회원가입 성공 시 돌아가 페이지로 향하는 view
    """
    return render(request, "success.html")


def login_home(request):
    """
    로그인, 회원가입을 진행할 페이지로 향하는 view
    """
    return render(request, "login_home.html")


def signup_info(request):
    return render(request, "signup_info.html")


def signup_email(request):
    """
    일반(이메일) 회원가입 처리해주는 view
    이메일 회원가입 완료 후 로그인 페이지로 향함
    """
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        email_remain = form["email"].value()
        if form.is_valid():
            user = form.save()  # 유저정보 저장
            login(
                request, user, backend="user.kakaobackends.KakaoBackend"
            )  # authenticate
            infoform = Emailform()
            return render(request, "signup_info.html", {"form": infoform})
        else:
            form = UserSignupForm(request.POST)
            return render(request, "signup_email.html", {"form": form, "email_remain":email_remain})
    else:
        form = UserSignupForm()
    return render(request, "signup_email.html", {"form": form})
    # email, password, is_kakao, name, kakao_id , major, phone_number, student_id


def email_login(request):
    """
    일반(이메일) 회원가입 처리해주는 view
    로그인 완료 후 로그인 성공 시 이동할 페이지로 향함 (상의 필요)
    """
    if request.method == "POST":
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            if form.authenticate_login():
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(
                        request, user, backend="user.kakaobackends.KakaoBackend"
                    )
                    return redirect("user_info")

            else :
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")
                user = authenticate(email=email, password=password)
                if len(CustomUser.objects.filter(email=email))==0:
                    return render(
                        request,
                        "email_login.html", 
                        {
                            "form": EmailAuthenticationForm(), 
                            "error_email" : "error_email"
                        } )
                else:
                    return render(
                        request,
                        "email_login.html",
                        {
                            "form": EmailAuthenticationForm(), 
                            "error_pw" : "error_pw"
                        } )
    else:
        form = EmailAuthenticationForm()
    return render(request, "email_login.html", {"form": form})


def kakao_login(request):
    """
    
    """
    if request.user.is_authenticated:
        return redirect("user_info")
    rest_api_key = settings.KAKAO_REST_API_KEY
    redirect_uri = "http://127.0.0.1:8000/user/kakao/login/callback/"
    state = "none"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={redirect_uri}&response_type=code&state={state}"
    )


def submit_kakao(request):
    """
    카카오/일반 회원가입 후 추가 정보 받고 유저에 저장하는 뷰입니다
    처음엔 카카오만 그 대상이었어서 ㅠㅠ 이름 헷갈리게 지은 점 죄송합니다
    """
    if not request.user.is_authenticated:
        return redirect("email_login")
    form = Emailform(request.POST, instance=request.user)
    if request.method == "POST":
        form = Emailform(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user_info")
    return render(request, "signup_info.html", {"form": form})


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
    res = requests.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "client_id": rest_api_key,
            "redirect_uri": redirect_uri,
            "code": code,
        },
    )
    token_response = res.json()
    access_token = token_response.get("access_token")
    info_url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"secure_resource": True}
    info_res = requests.get(info_url, headers=headers, params=params)

    try:
        info = info_res.json()
    except:
        info = None
    kakao_id = str(info.get("id"))

    try:
        test = CustomUser.objects.get(kakao_id=kakao_id)
    except CustomUser.DoesNotExist:
        test = None

    if test is None:
        personal_info = info.get("kakao_account")
        agree_on_nickname = personal_info.get("profile_needs_agreement")
        if not agree_on_nickname:
            profile = personal_info.get("profile")
            name = profile.get("nickname")
        agree_on_email = personal_info.get("email_needs_agreement")

        if not agree_on_email:

            email = personal_info.get("email")
        else:
            form = UserSignupForm
            return render(
                request,
                "signup_email.html",
                {"form": form, "error_code": "kakao_error"},
            )
        user = CustomUser.objects.create_user(
            email,
            None,
            True,
            name,
            kakao_id,
            "major",
            "phone_number",
            "student_id",
            "position",
        )
        form = (
            Emailform()
        )  # email, password, is_kakao, name, kakao_id , major, phone_number, student_id
        login(
            request, user, backend="user.kakaobackends.KakaoBackend"
        )  # 카카오 이메일을 안받는다면
        return render(request, "signup_info.html", {"form": form})

    else:
        login(
            request,
            CustomUser.objects.get(kakao_id=kakao_id),
            backend="user.kakaobackends.KakaoBackend",
        )
        if state == "none":
            return redirect("user_info")  # TO-DO : 우선은 로그인 완료 후 임시 페이지로 이동하게 함
        else:
            return redirect("user_info")


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
        headers = {"Authorization": f"KakaoAK {kakao_admin_key}"}
        data = {"target_id_type": "user_id", "target_id": target_id}
        logout_res = requests.post(
            logout_url, headers=headers, data=data
        ).json()
        response = logout_res.get("id")
        if target_id != response:
            return Exception("Kakao Logout failed")
        else:
            print(str(response) + "Kakao Logout successed")
    logout(request)
    return redirect("index")


def logout_with_kakao(request):
    """
    카카오톡과 함께 로그아웃 처리
    """
    kakao_rest_api_key = settings.KAKAO_REST_API_KEY
    logout_redirect_uri = "http://127.0.0.1:8000/user/logout/"
    state = "none"
    kakao_service_logout_url = "https://kauth.kakao.com/oauth/logout"
    return redirect(
        f"{kakao_service_logout_url}?client_id={kakao_rest_api_key}&logout_redirect_uri={logout_redirect_uri}&state={state}"
    )


def delete_user(request, user_pk):
    """
    탈퇴하기
    """
    user = request.user
    if user.pk == user_pk:
        if user.is_kakao:
            kakao_admin_key = settings.KAKAO_ADNIN_KEY
            user_kakao_id = int(user.kakao_id)
            url = "https://kapi.kakao.com/v1/user/unlink"
            headers = {"Authorization": f"KakaoAK {kakao_admin_key}"}
            data = {"target_id_type": "user_id", "target_id": user_kakao_id}
            res = requests.post(url, headers=headers, data=data)
            deleted_user_id = res.json().get("id")
            if deleted_user_id == user_kakao_id:
                print("연결 끊기 성공")
            else:
                print("연결끊기 실패")
        logout(request)
        user.delete()
        return redirect("login_home")
    else:
        raise ValidationError("잘못된 접근입니다.")


# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": self.title, **(self.extra_context or {})})
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = "user/registration/password_reset_email.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    template_name = "user/registration/password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        try:
            user_instance = CustomUser.objects.get(
            email=self.request.POST.get("email")
        )
        except CustomUser.DoesNotExist:
            return render(
                self.request,
                "user/registration/password_reset_form.html",
                {"form": form, "email_error":"email_error"},
            )
        
        if user_instance.has_usable_password():
            opts = {
                "use_https": self.request.is_secure(),
                "token_generator": self.token_generator,
                "from_email": self.from_email,
                "email_template_name": self.email_template_name,
                "subject_template_name": self.subject_template_name,
                "request": self.request,
                "html_email_template_name": self.html_email_template_name,
                "extra_email_context": self.extra_email_context,
            }
            form.save(**opts)
            return render(
                self.request,
                "user/registration/password_reset_done.html",
                {"form": form},
            )
        else:
            return render(
                self.request,
                "user/registration/password_reset_form.html",
                {"form": form, "kakao_error":"kakao_error"},
            )


INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = "user/registration/password_reset_done.html"
    title = _("Password reset sent")


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = "set-password"
    success_url = reverse_lazy("password_reset_complete")
    template_name = "user/registration/password_reset_confirm.html"
    title = _("Enter new password")
    token_generator = default_token_generator
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if token == self.reset_url_token:
                session_token = self.request.session.get(
                    INTERNAL_RESET_SESSION_TOKEN
                )
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            CustomUser.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context["validlink"] = True
        else:
            context.update(
                {
                    "form": None,
                    "title": _("Password reset unsuccessful"),
                    "validlink": False,
                }
            )
        return context


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = "user/registration/password_reset_complete.html"
    title = _("Password reset complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context

