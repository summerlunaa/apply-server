from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Application
from .forms import ApplicationForm, UserPositionForm


def index(request):
    return render(request, "home.html")


def applySuccess(request):
    return render(request, "application-success.html")


@login_required
def user_info(request):
    user = request.user
    if request.method == "POST":
        user_form = UserPositionForm(request.POST, instance=user)

        print("unvaild")
        print(user_form.is_valid())
        if user_form.is_valid():
            print("vaild")
            user_form.save()

        return redirect("application")

    else:
        user_form = UserPositionForm(instance=user)
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
