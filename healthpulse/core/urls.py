from django.contrib import admin
from django.urls import path
from .views import register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
]
