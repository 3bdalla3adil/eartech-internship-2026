from django.http import HttpResponse
from django.shortcuts import render

from accounts.decorators import instructor_required


def course_list(request):
    return HttpResponse('Courses app is working ✅')


@instructor_required
def creator_studio(request):
    """Instructor-only landing page for course management."""
    return render(request, "courses/creator_studio.html")
