import re
from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.db import models


YOUTUBE_VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")


def embed_url(url):
    """Return a safe YouTube/Vimeo embed URL, or None for unsupported URLs."""
    if not isinstance(url, str) or not url.strip():
        return None

    try:
        parsed = urlparse(url.strip())
        host = (parsed.hostname or "").lower()
    except ValueError:
        return None

    if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password:
        return None

    video_id = None

    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        elif parsed.path.startswith("/embed/"):
            parts = parsed.path.strip("/").split("/")
            if len(parts) == 2:
                video_id = parts[1]

        if video_id and YOUTUBE_VIDEO_ID.fullmatch(video_id):
            return f"https://www.youtube.com/embed/{video_id}"

    elif host == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]
        if YOUTUBE_VIDEO_ID.fullmatch(video_id):
            return f"https://www.youtube.com/embed/{video_id}"

    elif host in {"vimeo.com", "www.vimeo.com", "player.vimeo.com"}:
        parts = parsed.path.strip("/").split("/")
        if host == "player.vimeo.com" and len(parts) == 2 and parts[0] == "video":
            video_id = parts[1]
        elif parts:
            video_id = parts[0]

        if video_id and video_id.isdigit():
            return f"https://player.vimeo.com/video/{video_id}"

    return None


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)

    subtitle = models.CharField(max_length=250, blank=True)

    description = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="courses",
        null=True,
        blank=True,
    )

    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    thumbnail = models.ImageField(
        upload_to="thumbnails/",
        blank=True,
    )

    is_published = models.BooleanField(default=False)

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='enrollments.Enrollment',
        related_name='enrolled_courses'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class Module(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    @property
    def embed(self):
        return embed_url(self.video_url)


    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"
