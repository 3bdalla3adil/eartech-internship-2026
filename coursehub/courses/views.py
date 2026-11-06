from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Course
from .forms import CourseForm
from accounts.decorators import instructor_required


def course_list(request):
    return HttpResponse('Courses app is working ✅')


def home(request):
    courses = (
        Course.objects.filter(is_published=True)
        .select_related("instructor")
        .order_by("-created_at")[:8]
    )
    return render(request, "home.html", {"courses": courses})


@instructor_required
def add_course(request):
    form = CourseForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect("home")

    return render(request, "courses/add_course.html", {"form": form})