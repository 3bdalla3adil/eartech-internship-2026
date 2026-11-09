from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import instructor_required
from .models import Course


def course_list(request):
    return HttpResponse('Courses app is working ✅')


def home(request):
    courses = (
        Course.objects.filter(status=Course.Status.PUBLISHED)
        .select_related("instructor")
        .order_by("-created_at")[:8]
    )
    return render(request, "home.html", {"courses": courses})


@instructor_required
@require_POST
def toggle_publish(request, pk):
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    if course.status == Course.Status.PUBLISHED:
        course.status = Course.Status.DRAFT
    else:
        course.status = Course.Status.PUBLISHED
    course.save(update_fields=["status"])
    return redirect("home")


