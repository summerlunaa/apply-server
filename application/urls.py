from django.urls import path
from .views import *


urlpatterns = [
    path('application/', write, name="application"),
    # path('login/home/', login_home, name="login_home"),