from django import forms

from .models import Lesson, Module


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ["title", "order"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "notes", "video_url", "order"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "video_url": forms.URLInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }
