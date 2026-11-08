from django.urls import path

from . import views

from django.urls import path

from .views import (
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

    # Modules
    path(
        "courses/<int:course_id>/modules/add/",
        ModuleCreateView.as_view(),
        name="module-create",
    ),
    path(
        "modules/<int:pk>/edit/",
        ModuleUpdateView.as_view(),
        name="module-update",
    ),
    path(
        "modules/<int:pk>/delete/",
        ModuleDeleteView.as_view(),
        name="module-delete",
    ),

    # Lessons
    path(
        "modules/<int:module_id>/lessons/add/",
        LessonCreateView.as_view(),
        name="lesson-create",
    ),
    path(
        "lessons/<int:pk>/edit/",
        LessonUpdateView.as_view(),
        name="lesson-update",
    ),
    path(
        "lessons/<int:pk>/delete/",
        LessonDeleteView.as_view(),
        name="lesson-delete",
    ),
]