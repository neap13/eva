from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clinica.site_urls')),    # sitio (HTML)
    path('api/', include('clinica.api_urls')), # API + docs
]
