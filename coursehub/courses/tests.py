
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
            price=Decimal("49"), status="PUBLISHED",
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Python for Beginners")
        self.assertContains(response, "by Omar Ali")
        self.assertContains(response, "$49.00")

    def test_instructor_without_full_name_shows_username(self):
        sami = get_user_model().objects.create_user(username="sami", password="pass")
        Course.objects.create(title="Cyber 101", instructor=sami, status="PUBLISHED")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "by sami")

    def test_zero_price_shows_free(self):
        Course.objects.create(
            title="Cyber 101", instructor=self.omar,
            price=Decimal("0"), status="PUBLISHED",
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Free")

    def test_draft_courses_hidden(self):
        Course.objects.create(title="Draft Course", instructor=self.omar, status="DRAFT")
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "Draft Course")

    def test_placeholder_when_no_thumbnail(self):
        Course.objects.create(title="No Image", instructor=self.omar, status="PUBLISHED")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "placehold.co")

    def test_limits_to_eight_courses(self):
        for i in range(10):
            Course.objects.create(title=f"Course {i}", instructor=self.omar, status="PUBLISHED")
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
        

class TogglePublishTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.teacher = User.objects.create_user(
            username="teach", password="pass", role="INSTRUCTOR"
        )
        self.course = Course.objects.create(title="Django Web", instructor=self.teacher)
        self.url = reverse("courses:toggle_publish", args=[self.course.pk])

    def test_publish_then_unpublish(self):
        self.client.login(username="teach", password="pass")
        self.client.post(self.url)
        self.course.refresh_from_db()
        self.assertEqual(self.course.status, "PUBLISHED")
        self.client.post(self.url)
        self.course.refresh_from_db()
        self.assertEqual(self.course.status, "DRAFT")

    def test_other_instructor_cannot_toggle(self):
        get_user_model().objects.create_user(
            username="other", password="pass", role="INSTRUCTOR"
        )
        self.client.login(username="other", password="pass")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
