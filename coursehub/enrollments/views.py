from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def my_learning(request):
    """Student landing page for enrolled courses."""
    return render(request, "enrollments/my_learning.html")
