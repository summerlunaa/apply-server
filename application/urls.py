from django.urls import path
from . import views


urlpatterns = [
    path('application/', views.write, name="application"),
]