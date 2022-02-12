from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Application
from .forms import ApplicationForm, UserPositionForm
from user.forms import EmailAuthenticationForm, Emailform


def index(request):
    return render(request, "home.html")


def applySuccess(request):
    return render(request, "application-success.html")


@login_required(login_url="/user/login/email/")  # 로그인 안된 상태라면 로그인 페이지로
def user_info(request):
    user = request.user
    if request.method == "POST":
        user_form = UserPositionForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()

        return redirect("application")

    else:
        user_form = UserPositionForm(instance=user)
        if (
            request.user.name == "name"
            or request.user.student_id == "student_id"
            or user.major == "major"
        ):
            form = Emailform()
            return render(request, "signup_info.html", {"form": form})

    return render(request, "user_info.html", {"user_form": user_form})


@login_required
def write_application(request):
    application = Application.objects.filter(user=request.user).first()

    if request.method == "POST":
        if application:  # 지원서 수정
            form = ApplicationForm(
                request.POST, request.FILES, instance=application
            )
        else:  # 지원서 첫 작성
            form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            editApplication = form.save(commit=False)
            editApplication.user = request.user
            editApplication.updated_at = timezone.now()
            editApplication.save()
            return redirect("application-success")
    else:
        if application:  # 지원서 수정
            form = ApplicationForm(instance=application)
        else:  # 지원서 첫 작성
            form = ApplicationForm()
    return render(
        request, "application.html", {"form": form, "application": application}
    )
