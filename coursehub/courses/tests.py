from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth import get_user_model
from .models import Course, Module, Lesson

class CourseListViewTests(TestCase):
    def test_course_list_page_loads(self):
        response = self.client.get(reverse('courses:list'))
        self.assertEqual(response.status_code, 200)

class HomeViewTests(TestCase):
    def setUp(self):
        self.omar = get_user_model().objects.create_user(
            username="omar",
            password="pass",
            first_name="Omar",
            last_name="Ali",
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_card_shows_title_instructor_and_price(self):
        Course.objects.create(
            title="Python for Beginners", instructor=self.omar,
            price=Decimal("49"), is_published=True,
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Python for Beginners")
        self.assertContains(response, "by Omar Ali")
        self.assertContains(response, "$49.00")

    def test_instructor_without_full_name_shows_username(self):
        sami = get_user_model().objects.create_user(username="sami", password="pass")
        Course.objects.create(title="Cyber 101", instructor=sami, is_published=True)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "by sami")

    def test_zero_price_shows_free(self):
        Course.objects.create(
            title="Cyber 101", instructor=self.omar,
            price=Decimal("0"), is_published=True,
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Free")

    def test_draft_courses_hidden(self):
        Course.objects.create(title="Draft Course", instructor=self.omar, is_published=False)
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "Draft Course")

    def test_placeholder_when_no_thumbnail(self):
        Course.objects.create(title="No Image", instructor=self.omar, is_published=True)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "placehold.co")

    def test_limits_to_eight_courses(self):
        for i in range(10):
            Course.objects.create(title=f"Course {i}", instructor=self.omar, is_published=True)
        response = self.client.get(reverse("home"))
        self.assertEqual(len(response.context["courses"]), 8)

    def test_empty_state(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "No courses yet.")



class CourseCurriculumTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.instructor = User.objects.create_user(
            username="instructor1",
            password="testpass123",
            role="INSTRUCTOR",
        )

        self.other_instructor = User.objects.create_user(
            username="instructor2",
            password="testpass123",
            role="INSTRUCTOR",
        )

        self.course = Course.objects.create(
            title="Python for Beginners",
            instructor=self.instructor,
            is_published=True,
        )

        self.module = Module.objects.create(
            course=self.course,
            title="Introduction to Python",
            order=1,
        )

        self.lesson = Lesson.objects.create(
            module=self.module,
            title="What is Python?",
            notes="Introduction to Python programming",
            order=1,
        )

    def test_instructor_can_view_own_curriculum(self):
        self.client.login(username="instructor1", password="testpass123")

        response = self.client.get(
            reverse("courses:curriculum", args=[self.course.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python for Beginners")
        self.assertContains(response, "Introduction to Python")
        self.assertContains(response, "What is Python?")

    def test_other_instructor_gets_404(self):
        self.client.login(username="instructor2", password="testpass123")

        response = self.client.get(
            reverse("courses:curriculum", args=[self.course.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(
            reverse("courses:curriculum", args=[self.course.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)


class CurriculumCrudTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.instructor = User.objects.create_user(
            username="owner",
            password="testpass123",
            role="INSTRUCTOR",
        )
        self.other_instructor = User.objects.create_user(
            username="other",
            password="testpass123",
            role="INSTRUCTOR",
        )
        self.student = User.objects.create_user(
            username="student",
            password="testpass123",
            role="STUDENT",
        )

        self.course = Course.objects.create(
            title="Django for Beginners",
            instructor=self.instructor,
        )
        self.module = Module.objects.create(
            course=self.course,
            title="Getting Started",
            order=1,
        )
        self.lesson = Lesson.objects.create(
            module=self.module,
            title="Installing Python",
            notes="Setup guide",
            order=1,
        )

    def login_owner(self):
        self.client.login(username="owner", password="testpass123")

    def login_other(self):
        self.client.login(username="other", password="testpass123")

    def login_student(self):
        self.client.login(username="student", password="testpass123")

    # ----- curriculum page ------------------------------------------------

    def test_curriculum_shows_module_and_lesson_actions(self):
        self.login_owner()
        response = self.client.get(
            reverse("courses:curriculum", args=[self.course.id])
        )

        self.assertContains(response, "+ Add Module")
        self.assertContains(response, "+ Lesson")
        self.assertContains(
            response,
            reverse("courses:module_create", args=[self.course.id]),
        )
        self.assertContains(
            response,
            reverse("courses:module_edit", args=[self.module.id]),
        )
        self.assertContains(
            response,
            reverse("courses:module_delete", args=[self.module.id]),
        )
        self.assertContains(
            response,
            reverse("courses:lesson_create", args=[self.module.id]),
        )
        self.assertContains(
            response,
            reverse("courses:lesson_edit", args=[self.lesson.id]),
        )
        self.assertContains(
            response,
            reverse("courses:lesson_delete", args=[self.lesson.id]),
        )

    # ----- modules --------------------------------------------------------

    def test_module_create_form_loads(self):
        self.login_owner()
        response = self.client.get(
            reverse("courses:module_create", args=[self.course.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "courses/module_form.html")

    def test_instructor_can_create_module(self):
        self.login_owner()
        response = self.client.post(
            reverse("courses:module_create", args=[self.course.id]),
            {"title": "Advanced Topics", "order": 2},
        )

        self.assertRedirects(
            response,
            reverse("courses:curriculum", args=[self.course.id]),
        )
        module = Module.objects.get(title="Advanced Topics")
        self.assertEqual(module.course, self.course)

    def test_module_create_requires_ownership(self):
        self.login_other()
        response = self.client.post(
            reverse("courses:module_create", args=[self.course.id]),
            {"title": "Hijacked", "order": 3},
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(Module.objects.filter(title="Hijacked").exists())

    def test_module_create_requires_instructor_role(self):
        self.login_student()
        response = self.client.post(
            reverse("courses:module_create", args=[self.course.id]),
            {"title": "Student module", "order": 3},
        )

        self.assertEqual(response.status_code, 403)

    def test_module_create_requires_login(self):
        response = self.client.get(
            reverse("courses:module_create", args=[self.course.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_instructor_can_edit_module(self):
        self.login_owner()
        response = self.client.post(
            reverse("courses:module_edit", args=[self.module.id]),
            {"title": "Getting Started with Django", "order": 1},
        )

        self.assertRedirects(
            response,
            reverse("courses:curriculum", args=[self.course.id]),
        )
        self.module.refresh_from_db()
        self.assertEqual(self.module.title, "Getting Started with Django")

    def test_module_edit_requires_ownership(self):
        self.login_other()
        response = self.client.post(
            reverse("courses:module_edit", args=[self.module.id]),
            {"title": "Hijacked", "order": 1},
        )

        self.assertEqual(response.status_code, 404)
        self.module.refresh_from_db()
        self.assertEqual(self.module.title, "Getting Started")

    def test_module_delete_confirmation_page(self):
        self.login_owner()
        response = self.client.get(
            reverse("courses:module_delete", args=[self.module.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "courses/confirm_delete.html")
        self.assertContains(response, "Getting Started")
        self.assertContains(response, "Every lesson inside this module")

    def test_delete_module_get_does_not_delete(self):
        self.login_owner()
        self.client.get(
            reverse("courses:module_delete", args=[self.module.id])
        )

        self.assertTrue(Module.objects.filter(id=self.module.id).exists())

    def test_instructor_can_delete_module(self):
        self.login_owner()
        response = self.client.post(
            reverse("courses:module_delete", args=[self.module.id])
        )

        self.assertRedirects(
            response,
            reverse("courses:curriculum", args=[self.course.id]),
        )
        self.assertFalse(Module.objects.filter(id=self.module.id).exists())
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_module_delete_requires_ownership(self):
        self.login_other()
        response = self.client.post(
            reverse("courses:module_delete", args=[self.module.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Module.objects.filter(id=self.module.id).exists())

    # ----- lessons --------------------------------------------------------

    def test_lesson_create_form_loads(self):
        self.login_owner()
        response = self.client.get(
            reverse("courses:lesson_create", args=[self.module.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "courses/lesson_form.html")
        self.assertContains(response, "Getting Started")

    def test_instructor_can_create_lesson(self):
        self.login_owner()
        response = self.client.post(
            reverse("courses:lesson_create", args=[self.module.id]),
            {
                "title": "Your first project",
                "notes": "Create the project",
                "video_url": "",
                "order": 2,
            },
        )

        self.assertRedirects(
            response,
            reverse("courses:curriculum", args=[self.course.id]),
        )
        lesson = Lesson.objects.get(title="Your first project")
        self.assertEqual(lesson.module, self.module)

    def test_lesson_create_requires_ownership(self):
        self.login_other()
        response = self.client.post(
            reverse("courses:lesson_create", args=[self.module.id]),
            {"title": "Hijacked lesson", "order": 2},
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(Lesson.objects.filter(title="Hijacked lesson").exists())

    def test_instructor_can_edit_lesson(self):
        self.login_owner()
        response = self.client.post(
            reverse("courses:lesson_edit", args=[self.lesson.id]),
            {
                "title": "Installing Python 3",
                "notes": "Updated notes",
                "video_url": "https://example.com/video",
                "order": 1,
            },
        )

        self.assertRedirects(
            response,
            reverse("courses:curriculum", args=[self.course.id]),
        )
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Installing Python 3")
        self.assertEqual(self.lesson.video_url, "https://example.com/video")

    def test_lesson_edit_requires_ownership(self):
        self.login_other()
        response = self.client.post(
            reverse("courses:lesson_edit", args=[self.lesson.id]),
            {"title": "Hijacked", "order": 1},
        )

        self.assertEqual(response.status_code, 404)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Installing Python")

    def test_lesson_delete_confirmation_page(self):
        self.login_owner()
        response = self.client.get(
            reverse("courses:lesson_delete", args=[self.lesson.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "courses/confirm_delete.html")
        self.assertContains(response, "Installing Python")

    def test_instructor_can_delete_lesson(self):
        self.login_owner()
        response = self.client.post(
            reverse("courses:lesson_delete", args=[self.lesson.id])
        )

        self.assertRedirects(
            response,
            reverse("courses:curriculum", args=[self.course.id]),
        )
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_delete_requires_ownership(self):
        self.login_other()
        response = self.client.post(
            reverse("courses:lesson_delete", args=[self.lesson.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_student_cannot_delete_lessons(self):
        self.login_student()
        response = self.client.post(
            reverse("courses:lesson_delete", args=[self.lesson.id])
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())
