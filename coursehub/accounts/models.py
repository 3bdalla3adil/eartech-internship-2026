
from django.contrib.auth.models import AbstractUser
from django.db import models

<<<<<<< HEAD
# Create your models here.
from django.contrib.auth.models import AbstractUser
=======
>>>>>>> f08b59dbc75e08e8d594e580c61328c1c1e6b932

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"
<<<<<<< HEAD
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
=======

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )
>>>>>>> f08b59dbc75e08e8d594e580c61328c1c1e6b932

    @property
    def is_instructor(self):
        return self.role == self.Role.INSTRUCTOR
<<<<<<< HEAD


=======
>>>>>>> f08b59dbc75e08e8d594e580c61328c1c1e6b932
