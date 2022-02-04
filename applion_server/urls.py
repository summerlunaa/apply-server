from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('', include('application.urls')),
    path('admin/', admin.site.urls),
    path('user/', include("user.urls")),
]
