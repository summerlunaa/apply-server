from django.contrib import admin
from django.urls import path, include
# for media files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('application.urls')),
    path('applion-admin97/', admin.site.urls),
    path('user/', include("user.urls")),
]

# for media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)