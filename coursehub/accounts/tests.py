from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.views import View

from accounts.decorators import InstructorRequiredMixin, instructor_required
from accounts.forms import RegisterForm

User = get_user_model()

PASSWORD = "Coursehub!2026pass"


# --- Dummy views for testing the permission helpers ---

@instructor_required
def dummy_view(request):
    return HttpResponse("OK")


class DummyViewClass(InstructorRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("OK")


class RoleChecksTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.instructor = User.objects.create_user(
            username="instructor_test",
            password="Password123!",
            role=User.Role.INSTRUCTOR,
        )
        self.student = User.objects.create_user(
            username="student_test",
            password="Password123!",
            role=User.Role.STUDENT,
        )

    # --- Decorator tests ---

    def test_instructor_access(self):
        request = self.factory.get("/dummy/")
        request.user = self.instructor
        response = dummy_view(request)
        self.assertEqual(response.status_code, 200)

    def test_student_access_forbidden(self):
        request = self.factory.get("/dummy/")
        request.user = self.student
        with self.assertRaises(PermissionDenied):
            dummy_view(request)

    def test_anonymous_redirect(self):
        request = self.factory.get("/dummy/")
        request.user = AnonymousUser()
        response = dummy_view(request)
        self.assertEqual(response.status_code, 302)

    # --- Mixin tests ---

    def test_mixin_instructor_access(self):
        request = self.factory.get("/dummy/")
        request.user = self.instructor
        response = DummyViewClass.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_mixin_student_access_forbidden(self):
        request = self.factory.get("/dummy/")
        request.user = self.student
        with self.assertRaises(PermissionDenied):
            DummyViewClass.as_view()(request)

    def test_mixin_anonymous_redirect(self):
        request = self.factory.get("/dummy/")
        request.user = AnonymousUser()
        response = DummyViewClass.as_view()(request)
        self.assertEqual(response.status_code, 302)


class RegistrationTests(TestCase):
    def payload(self, **overrides):
        data = {
            "username": "newstudent",
            "email": "newstudent@example.com",
            "role": User.Role.STUDENT,
            "password1": PASSWORD,
            "password2": PASSWORD,
        }
        data.update(overrides)
        return data

    def test_register_page_shows_the_form(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="role"')
        self.assertContains(response, "Create an account")

    def test_register_creates_a_student_and_logs_them_in(self):
        response = self.client.post(reverse("register"), self.payload())

        self.assertRedirects(response, reverse("dashboard"))
        user = User.objects.get(username="newstudent")
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertEqual(user.email, "newstudent@example.com")
        self.assertTrue(user.check_password(PASSWORD))
        self.assertIn("_auth_user_id", self.client.session)

    def test_register_cannot_create_an_instructor(self):
        response = self.client.post(
            reverse("register"), self.payload(role=User.Role.INSTRUCTOR)
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newstudent").exists())

    def test_register_rejects_duplicate_username(self):
        User.objects.create_user(username="newstudent", password=PASSWORD)
        response = self.client.post(reverse("register"), self.payload())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A user with that username already exists")

    def test_register_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("register"), self.payload(password2="Different!2026")
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newstudent").exists())
        self.assertContains(response, "The two password fields")

    def test_register_requires_an_email(self):
        response = self.client.post(reverse("register"), self.payload(email=""))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newstudent").exists())

    def test_register_form_exposes_the_role_field(self):
        self.assertIn("role", RegisterForm().fields)


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username="student1",
            password=PASSWORD,
            role=User.Role.STUDENT,
        )
        self.instructor = User.objects.create_user(
            username="teacher1",
            password=PASSWORD,
            role=User.Role.INSTRUCTOR,
        )

    def test_student_login_redirects_to_dashboard(self):
        response = self.client.post(
            reverse("login"), {"username": "student1", "password": PASSWORD}
        )
        self.assertRedirects(response, reverse("dashboard"))

    def test_instructor_login_redirects_to_dashboard(self):
        response = self.client.post(
            reverse("login"), {"username": "teacher1", "password": PASSWORD}
        )
        self.assertRedirects(response, reverse("dashboard"))

    def test_logout_redirects_home(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("home"))

    def test_login_page_links_to_registration(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, reverse("register"))


class RoleNavigationTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username="student1",
            password=PASSWORD,
            role=User.Role.STUDENT,
        )
        self.instructor = User.objects.create_user(
            username="teacher1",
            password=PASSWORD,
            role=User.Role.INSTRUCTOR,
        )

    def test_guest_sees_login_and_register_only(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, reverse("login"))
        self.assertContains(response, reverse("register"))
        self.assertNotContains(response, "Creator Studio")
        self.assertNotContains(response, "My Learning")

    def test_student_sees_my_learning_but_not_creator_studio(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("home"))

        self.assertContains(response, "My Learning")
        self.assertContains(response, reverse("enrollments:my_learning"))
        self.assertNotContains(response, "Creator Studio")
        self.assertContains(response, "student1")

    def test_instructor_sees_creator_studio_but_not_my_learning(self):
        self.client.force_login(self.instructor)
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Creator Studio")
        self.assertContains(response, reverse("courses:studio"))
        self.assertNotContains(response, "My Learning")
        self.assertContains(response, "teacher1")

    def test_navbar_logout_is_a_post_form(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("home"))

        self.assertContains(response, f'action="{reverse("logout")}"')
        self.assertContains(response, "Log out")


class ProtectedViewTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username="student1",
            password=PASSWORD,
            role=User.Role.STUDENT,
        )
        self.instructor = User.objects.create_user(
            username="teacher1",
            password=PASSWORD,
            role=User.Role.INSTRUCTOR,
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}",
            fetch_redirect_response=False,
        )

    def test_student_is_forbidden_from_creator_studio(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("courses:studio"))
        self.assertEqual(response.status_code, 403)

    def test_instructor_can_open_creator_studio(self):
        self.client.force_login(self.instructor)
        response = self.client.get(reverse("courses:studio"))
        self.assertEqual(response.status_code, 200)

    def test_guest_is_redirected_from_creator_studio(self):
        response = self.client.get(reverse("courses:studio"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('courses:studio')}",
            fetch_redirect_response=False,
        )

    def test_my_learning_requires_login(self):
        response = self.client.get(reverse("enrollments:my_learning"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('enrollments:my_learning')}",
            fetch_redirect_response=False,
        )

    def test_student_can_open_my_learning(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("enrollments:my_learning"))
        self.assertEqual(response.status_code, 200)
