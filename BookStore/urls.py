from Profile import urls as profile_urls
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Bookmanager.urls')),
    path('user/', include('User.urls')),
    path('profile/', include(profile_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
