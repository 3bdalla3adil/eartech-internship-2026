from django.http import HttpResponse
from django.shortcuts import render
from .models import Course


def course_list(request):
    return HttpResponse('Courses app is working ✅')

# Create your views here.
def home(request):
    courses = (
        Course.objects.filter(is_published=True)
        .select_related("instructor")
        .order_by("-created_at")[:8]
    )
    return render(request, "home.html", {"courses": courses})

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Course, Module, Lesson

class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    fields = ["title", "order"]

    def form_valid(self, form):
        course = Course.objects.get(pk=self.kwargs["course_id"])

        if course.instructor != self.request.user:
            return self.handle_no_permission()

        form.instance.course = course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "course-detail",
            kwargs={"pk": self.object.course.pk}
        )

class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    fields = ["title", "order"]

    def form_valid(self, form):
        course = Course.objects.get(pk=self.kwargs["course_id"])

        if course.instructor != self.request.user:
            return self.handle_no_permission()

        form.instance.course = course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "course-detail",
            kwargs={"pk": self.object.course.pk}
        )

class ModuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Module
    fields = ["title", "order"]

    def get_queryset(self):
        return Module.objects.filter(
            course__instructor=self.request.user
        )

    def get_success_url(self):
        return reverse_lazy(
            "course-detail",
            kwargs={"pk": self.object.course.pk}
        )

class ModuleDeleteView(LoginRequiredMixin, DeleteView):
    model = Module

    def get_queryset(self):
        return Module.objects.filter(
            course__instructor=self.request.user
        )

    def get_success_url(self):
        return reverse_lazy(
            "course-detail",
            kwargs={"pk": self.object.course.pk}
        )

class LessonUpdateView(LoginRequiredMixin, UpdateView):
    model = Lesson
    fields = [
        "title",
        "notes",
        "video_url",
        "order",
    ]

    def get_queryset(self):
        return Lesson.objects.filter(
            module__course__instructor=self.request.user
        )

    def get_success_url(self):
        return reverse_lazy(
            "course-detail",
            kwargs={"pk": self.object.module.course.pk}
        )

class LessonDeleteView(LoginRequiredMixin, DeleteView):
    model = Lesson

    def get_queryset(self):
        return Lesson.objects.filter(
            module__course__instructor=self.request.user
        )

    def get_success_url(self):
        return reverse_lazy(
            "course-detail",
            kwargs={"pk": self.object.module.course.pk}
        )

