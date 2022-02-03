from django.urls import path
from .views import *


urlpatterns= [

    path('login/home/', login_home, name="login_home"),

    path('login/kakao/', kakao_login, name="kakao_login"),
    path('kakao/login/callback/', kakao_login_callback, name="kakao_login_callback"), 
    path('kakao/submit/', submit_kakao, name="submit_kakao"),

    path('logout/', logout_view, name="logout"), 
    path('logout/with/kakao', logout_with_kakao, name="logout_with_kakao"),

    path('success/', success, name = "success"),
]