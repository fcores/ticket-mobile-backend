"""
URL configuration for helpdesk project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.authentication.urls')),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.tickets.urls')),
    path('api/', include('apps.comments.urls')),
    path('api/', include('apps.attachments.urls')),
    path('api/', include('apps.categories.urls')),
    path('api/', include('apps.metrics.urls')),
    path('api/', include('apps.common.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
