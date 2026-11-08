
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .forms import validate_thumbnail_size
from .models import Course


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


class ThumbnailSizeValidationTests(TestCase):
    def test_rejects_image_larger_than_2_mb(self):
        image = SimpleUploadedFile(
            "large.jpg",
            b"x" * (2 * 1024 * 1024 + 1),
            content_type="image/jpeg",
        )

        with self.assertRaises(ValidationError):
            validate_thumbnail_size(image)

    def test_accepts_image_smaller_than_2_mb(self):
        image = SimpleUploadedFile(
            "small.jpg",
            b"x" * 1024,
            content_type="image/jpeg",
        )
        self.assertIs(validate_thumbnail_size(image), image)


from courses.models import Course, Module, Lesson

User = get_user_model()


class ModuleLessonModelTests(TestCase):

    def setUp(self):
        self.instructor = User.objects.create_user(
            username="instructor",
            password="password123"
        )

        self.course = Course.objects.create(
            title="Python Course",
            instructor=self.instructor
        )

    def test_create_module_for_course(self):
        module = Module.objects.create(
            course=self.course,
            title="Introduction",
            order=1
        )

        self.assertEqual(module.course, self.course)

    def test_module_ordering(self):
        Module.objects.create(
            course=self.course,
            title="Module 2",
            order=2
        )

        Module.objects.create(
            course=self.course,
            title="Module 1",
            order=1
        )

        modules = list(Module.objects.all())

        self.assertEqual(modules[0].title, "Module 1")
        self.assertEqual(modules[1].title, "Module 2")

    def test_create_lesson_for_module(self):
        module = Module.objects.create(
            course=self.course,
            title="Introduction",
            order=1
        )

        lesson = Lesson.objects.create(
            module=module,
            title="Lesson 1",
            notes="Lesson notes",
            video_url="https://youtube.com/watch?v=test",
            order=1
        )

        self.assertEqual(lesson.module, module)

    def test_lesson_ordering(self):
        module = Module.objects.create(
            course=self.course,
            title="Introduction",
            order=1
        )

        Lesson.objects.create(
            module=module,
            title="Lesson 2",
            order=2
        )

        Lesson.objects.create(
            module=module,
            title="Lesson 1",
            order=1
        )

        lessons = list(module.lessons.all())

        self.assertEqual(lessons[0].title, "Lesson 1")
        self.assertEqual(lessons[1].title, "Lesson 2")

    def test_lesson_optional_notes(self):
        module = Module.objects.create(
            course=self.course,
            title="Introduction",
            order=1
        )

        lesson = Lesson.objects.create(
            module=module,
            title="Lesson 1",
            order=1
        )

        self.assertEqual(lesson.notes, "")

    def test_lesson_optional_video_url(self):
        module = Module.objects.create(
            course=self.course,
            title="Introduction",
            order=1
        )

        lesson = Lesson.objects.create(
            module=module,
            title="Lesson 1",
            order=1
        )

        self.assertIsNone(lesson.video_url)

    def test_valid_video_url(self):
        module = Module.objects.create(
            course=self.course,
            title="Introduction",
            order=1
        )

        lesson = Lesson(
            module=module,
            title="Lesson 1",
            video_url="https://youtube.com/watch?v=test"
        )

        lesson.full_clean()

    def test_invalid_video_url(self):
        module = Module.objects.create(
            course=self.course,
            title="Introduction",
            order=1
        )

        lesson = Lesson(
            module=module,
            title="Lesson 1",
            video_url="invalid-url"
        )

        with self.assertRaises(ValidationError):
            lesson.full_clean()

class ModulePermissionTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="password123"
        )

        self.other_user = User.objects.create_user(
            username="other",
            password="password123"
        )

        self.course = Course.objects.create(
            title="Python Course",
            instructor=self.owner
        )

        self.module = Module.objects.create(
            course=self.course,
            title="Module 1",
            order=1
        )

    def test_owner_can_update_module(self):
        self.client.login(
            username="owner",
            password="password123"
        )

        response = self.client.post(
            reverse("module-update", args=[self.module.pk]),
            {
                "title": "Updated Module",
                "order": 1,
            }
        )

        self.module.refresh_from_db()

        self.assertEqual(self.module.title, "Updated Module")

    def test_non_owner_cannot_update_module(self):
        self.client.login(
            username="other",
            password="password123"
        )

        response = self.client.post(
            reverse("module-update", args=[self.module.pk]),
            {
                "title": "Hacked Module",
                "order": 1,
            }
        )

        self.module.refresh_from_db()

        self.assertNotEqual(
            self.module.title,
            "Hacked Module"
        )

        self.assertIn(response.status_code, [403, 404])

    def test_owner_can_delete_module(self):
        self.client.login(
            username="owner",
            password="password123"
        )

        self.client.post(
            reverse("module-delete", args=[self.module.pk])
        )

        self.assertFalse(
            Module.objects.filter(
                pk=self.module.pk
            ).exists()
        )

    def test_non_owner_cannot_delete_module(self):
        self.client.login(
            username="other",
            password="password123"
        )

        response = self.client.post(
            reverse("module-delete", args=[self.module.pk])
        )

        self.assertTrue(
            Module.objects.filter(
                pk=self.module.pk
            ).exists()
        )

        self.assertIn(response.status_code, [403, 404])