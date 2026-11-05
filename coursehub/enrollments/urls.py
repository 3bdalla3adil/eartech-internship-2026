from django.urls import path

from . import views

app_name = 'enrollments'

urlpatterns = [
    path('', views.my_learning, name='my_learning'),
]
