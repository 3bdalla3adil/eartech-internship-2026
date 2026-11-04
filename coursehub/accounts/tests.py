from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views import View
# هنا قمنا بتصحيح مسار الاستيراد ليجلب الاثنين من decorators
from accounts.decorators import instructor_required, InstructorRequiredMixin

User = get_user_model()

# --- Dummy views for testing ---

@instructor_required
def dummy_view(request):
    return HttpResponse("OK")

class DummyViewClass(InstructorRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("OK")

# --- Test Case ---

class RoleChecksTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.instructor = User.objects.create_user(
            username='instructor_test', 
            password='Password123!', 
            role='INSTRUCTOR'
        )
        self.student = User.objects.create_user(
            username='student_test', 
            password='Password123!', 
            role='STUDENT'
        )

    # --- Decorator Tests ---

    def test_instructor_access(self):
        request = self.factory.get('/dummy/')
        request.user = self.instructor
        response = dummy_view(request)
        self.assertEqual(response.status_code, 200)

    def test_student_access_forbidden(self):
        request = self.factory.get('/dummy/')
        request.user = self.student
        with self.assertRaises(PermissionDenied):
            dummy_view(request)

    def test_anonymous_redirect(self):
        request = self.factory.get('/dummy/')
        request.user = AnonymousUser()
        response = dummy_view(request)
        self.assertEqual(response.status_code, 302)

    # --- Mixin Tests ---

    def test_mixin_instructor_access(self):
        request = self.factory.get('/dummy/')
        request.user = self.instructor
        response = DummyViewClass.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_mixin_student_access_forbidden(self):
        request = self.factory.get('/dummy/')
        request.user = self.student
        with self.assertRaises(PermissionDenied):
            DummyViewClass.as_view()(request)

    def test_mixin_anonymous_redirect(self):
        request = self.factory.get('/dummy/')
        request.user = AnonymousUser()
        response = DummyViewClass.as_view()(request)
        self.assertEqual(response.status_code, 302)