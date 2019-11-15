from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    url(r'^patches/(?P<path>.*)$', serve, {'document_root': settings.PATCHES_ROOT})
]

# urlpatterns += static(settings.PATCHES_URL, document_root=settings.PATCHES_ROOT, show_indexes=True)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
