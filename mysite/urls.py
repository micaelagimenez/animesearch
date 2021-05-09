from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import core.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('django.contrib.auth.urls')),
    path('', include(core.urls)),
]
