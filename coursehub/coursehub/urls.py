from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from accounts import views as account_views
from accounts.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('courses/', include('courses.urls')),
    path('my-learning/', include('enrollments.urls')),
    path("dashboard/", account_views.dashboard, name="dashboard"),
    path("accounts/register/", account_views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=LoginForm,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
