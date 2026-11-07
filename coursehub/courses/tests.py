from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Category, Course

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

class CourseCreateUpdateTests(TestCase):
    """Course create/update views for instructors (AB#3301)."""

    def setUp(self):
        User = get_user_model()
        self.instructor = User.objects.create_user(
            username="lina",
            password="pass",
            role="INSTRUCTOR",
        )
        self.other_instructor = User.objects.create_user(
            username="omar",
            password="pass",
            role="INSTRUCTOR",
        )
        self.student = User.objects.create_user(
            username="student",
            password="pass",
            role="STUDENT",
        )
        self.category = Category.objects.get(name="Web Development")
        self.other_course = Course.objects.create(
            title="Omar's course",
            instructor=self.other_instructor,
            description="Owned by Omar.",
            category=self.category,
        )

    def login(self, username):
        self.client.login(username=username, password="pass")

    def payload(self, **overrides):
        data = {
            "title": "Django for Beginners",
            "subtitle": "Build your first web app",
            "category": self.category.pk,
            "price": "49.00",
            "description": "A beginner friendly Django course.",
            "thumbnail": "",
        }
        data.update(overrides)
        return data

    # ----- seeding --------------------------------------------------------

    def test_categories_are_seeded(self):
        names = set(Category.objects.values_list("name", flat=True))
        self.assertEqual(
            names,
            {"Web Development", "Cybersecurity", "AI", "Data"},
        )

    # ----- create ---------------------------------------------------------

    def test_create_form_loads_for_instructor(self):
        self.login("lina")
        response = self.client.get(reverse("courses:course_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "courses/course_form.html")
        self.assertContains(response, "Create New Course")
        self.assertContains(response, "Web Development")

    def test_instructor_can_create_course(self):
        self.login("lina")
        response = self.client.post(
            reverse("courses:course_create"),
            self.payload(),
        )

        self.assertRedirects(response, reverse("studio"))
        course = Course.objects.get(title="Django for Beginners")
        self.assertEqual(course.instructor, self.instructor)
        self.assertEqual(course.category, self.category)
        self.assertEqual(course.subtitle, "Build your first web app")
        self.assertFalse(course.is_published)

    def test_create_sets_owner_and_ignores_posted_instructor(self):
        self.login("lina")
        self.client.post(
            reverse("courses:course_create"),
            self.payload(instructor=self.other_instructor.pk),
        )

        course = Course.objects.get(title="Django for Beginners")
        self.assertEqual(course.instructor, self.instructor)

    def test_create_requires_description(self):
        self.login("lina")
        response = self.client.post(
            reverse("courses:course_create"),
            self.payload(description=""),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Course.objects.filter(title="Django for Beginners").exists()
        )

    def test_create_requires_instructor_role(self):
        self.login("student")
        response = self.client.get(reverse("courses:course_create"))

        self.assertEqual(response.status_code, 403)

    def test_create_requires_login(self):
        response = self.client.get(reverse("courses:course_create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    # ----- update ---------------------------------------------------------

    def test_own_course_form_is_prefilled(self):
        own_course = Course.objects.create(
            title="My course",
            instructor=self.instructor,
            description="Mine.",
            category=self.category,
        )
        self.login("lina")
        response = self.client.get(
            reverse("courses:course_update", args=[own_course.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My course")
        self.assertContains(response, "Edit Course")

    def test_instructor_can_update_own_course(self):
        own_course = Course.objects.create(
            title="My course",
            instructor=self.instructor,
            description="Mine.",
            category=self.category,
        )
        self.login("lina")
        response = self.client.post(
            reverse("courses:course_update", args=[own_course.pk]),
            self.payload(title="My updated course"),
        )

        self.assertRedirects(response, reverse("studio"))
        own_course.refresh_from_db()
        self.assertEqual(own_course.title, "My updated course")
        self.assertEqual(own_course.instructor, self.instructor)

    def test_cannot_update_another_instructors_course(self):
        self.login("lina")
        response = self.client.post(
            reverse("courses:course_update", args=[self.other_course.pk]),
            self.payload(title="Hijacked"),
        )

        self.assertEqual(response.status_code, 404)
        self.other_course.refresh_from_db()
        self.assertEqual(self.other_course.title, "Omar's course")

    def test_update_missing_course_returns_404(self):
        self.login("lina")
        response = self.client.get(
            reverse("courses:course_update", args=[99999])
        )

        self.assertEqual(response.status_code, 404)

    def test_update_requires_instructor_role(self):
        self.login("student")
        response = self.client.get(
            reverse("courses:course_update", args=[self.other_course.pk])
        )

        self.assertEqual(response.status_code, 403)

    # ----- studio ---------------------------------------------------------

    def test_studio_lists_only_own_courses(self):
        Course.objects.create(
            title="Lina's course",
            instructor=self.instructor,
            description="Mine.",
            category=self.category,
        )
        self.login("lina")
        response = self.client.get(reverse("studio"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lina&#x27;s course")
        self.assertNotContains(response, "Omar&#x27;s course")

    def test_studio_requires_instructor_role(self):
        self.login("student")
        response = self.client.get(reverse("studio"))

        self.assertEqual(response.status_code, 403)

    def test_studio_requires_login(self):
        response = self.client.get(reverse("studio"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
