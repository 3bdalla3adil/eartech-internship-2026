from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Registration
    path('register/', register_view, name='register'),

    # Login
    path('login/', LoginView.as_view(
        template_name='login.html'
    ), name='login'),

    # Logout
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]