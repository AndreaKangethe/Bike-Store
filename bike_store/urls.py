from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

# Serve media files during development or on Render ephemeral storage
if settings.DEBUG or os.environ.get("RENDER"):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
