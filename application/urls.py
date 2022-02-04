from django.urls import path
from .views import *


urlpatterns = [
    path('application/', write, name="application"),
    path('', index, name="index"),
]