from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name="index"),
    path('application/userinfo/', user_info, name="user_info"),
    path('application/write/', write_application, name="application"),
    path('application-success/', applySuccess, name="application-success"),

    # path('login/home/', login_home, name="login_home"),
]