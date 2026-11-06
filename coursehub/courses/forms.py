
from django import forms
from django.core.exceptions import ValidationError

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "price", "thumbnail", "is_published"]

    def clean_thumbnail(self):
        image = self.cleaned_data.get("thumbnail")

        if image and image.size > 2 * 1024 * 1024:
            raise ValidationError("Image must be under 2 MB.")

        return image
