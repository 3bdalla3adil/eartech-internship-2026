from django.contrib import admin
from .models import Course

from .models import Course, Lesson, Module


admin.site.register([Course, Module, Lesson])
