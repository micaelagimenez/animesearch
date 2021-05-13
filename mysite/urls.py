from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import core.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('django.contrib.auth.urls')),
    path('', include(core.urls)),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),      

]
