from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Application
from .forms import ApplicationForm


@login_required
def write(request):
    application = Application.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        if application: # 지원서 수정
            form = ApplicationForm(request.POST, request.FILES, instance=application)
        else:           # 지원서 첫 작성
            form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            editApplication = form.save(commit=False)
            editApplication.user = request.user
            editApplication.updated_at = timezone.now()
            editApplication.save()
            return redirect('application')
    else:
        if application: # 지원서 수정
            form = ApplicationForm(instance=application)
        else:           # 지원서 첫 작성
            form = ApplicationForm()
    return render(request, 'application.html', {'form': form})