from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='list'),
    path('<int:pk>/toggle-publish/', views.toggle_publish, name='toggle_publish'),
]
