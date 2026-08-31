from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Uniquement les APIs pour React
    path('api/auth/', include('apps.accounts.api_urls')),
    path('api/gallery/', include('apps.gallery.api_urls')),
    path('api/portfolio/', include('apps.portfolio.api_urls')),
    path('api/orders/', include('apps.orders.api_urls')),
    path('api/messaging/', include('apps.messaging.api_urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)