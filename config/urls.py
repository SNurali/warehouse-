from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('apps.tenants.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('orders/', include('apps.orders.urls')),
    path('reports/', include('apps.reporting.urls')),
    path('api/', include('apps.api.urls')),
    path('', include('apps.dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)