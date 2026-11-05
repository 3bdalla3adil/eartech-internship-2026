from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


def _add_bootstrap_classes(form):
    for field in form.fields.values():
        css_class = (
            "form-select"
            if isinstance(field.widget, forms.Select)
            else "form-control"
        )
        field.widget.attrs.setdefault("class", css_class)


class LoginForm(AuthenticationForm):
    """Standard login form with Bootstrap styling."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_classes(self)


class RegisterForm(UserCreationForm):
    """Public sign-up form.

    Registration only ever creates students. Instructor accounts are promoted by
    an administrator in the Django admin, so a visitor cannot grant themselves
    instructor permissions by editing the submitted form.
    """

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["role"].choices = [
            (User.Role.STUDENT, User.Role.STUDENT.label),
        ]
        self.fields["role"].initial = User.Role.STUDENT
        self.fields["role"].help_text = (
            "Instructor accounts are created by an administrator."
        )

        _add_bootstrap_classes(self)
