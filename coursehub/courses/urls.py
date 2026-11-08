from django.urls import path

from . import views

from django.urls import path

from .views import (
    CourseDetailView,
    ModuleCreateView,
    ModuleUpdateView,
    ModuleDeleteView,
    LessonCreateView,
    LessonUpdateView,
    LessonDeleteView,
)
app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='list'),

    path(
        "courses/<int:pk>/", 
        CourseDetailView.as_view(), 
        name="course_detail"
    ),
    # Modules
    path(
        "courses/<int:course_id>/modules/add/",
        ModuleCreateView.as_view(),
        name="module_create",
    ),
    path(
        "modules/<int:pk>/edit/",
        ModuleUpdateView.as_view(),
        name="module_update",
    ),
    path(
        "modules/<int:pk>/delete/",
        ModuleDeleteView.as_view(),
        name="module_delete",
    ),

    # Lessons
    path(
        "modules/<int:module_id>/lessons/add/",
        LessonCreateView.as_view(),
        name="lesson_create",
    ),
    path(
        "lessons/<int:pk>/edit/",
        LessonUpdateView.as_view(),
        name="lesson_update",
    ),
    path(
        "lessons/<int:pk>/delete/",
        LessonDeleteView.as_view(),
        name="lesson_delete",
    ),
]