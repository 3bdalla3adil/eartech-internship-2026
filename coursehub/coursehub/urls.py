
"""
URL configuration for coursehub project.
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib.auth import views as auth_views
from accounts.views import register
from courses.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path('courses/', include('courses.urls')),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/register/", register, name="register"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
